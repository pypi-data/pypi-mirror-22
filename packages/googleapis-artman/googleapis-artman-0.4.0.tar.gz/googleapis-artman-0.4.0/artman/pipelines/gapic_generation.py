# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Pipelines that run GAPIC code generation."""

from __future__ import absolute_import
import importlib

from artman.pipelines import code_generation as code_gen
from artman.pipelines import grpc_generation as grpc_gen
from artman.pipelines import batch_generation as batch_gen
from artman import tasks
from artman.utils import task_utils


# kwargs required by GAPIC code gen
_GAPIC_REQUIRED = ['service_yaml', 'gapic_language_yaml', 'gapic_api_yaml',
                   'gapic_code_dir', 'language', 'publish']


class GapicConfigPipeline(code_gen.CodeGenerationPipelineBase):

    def __init__(self, **kwargs):
        super(GapicConfigPipeline, self).__init__(
            GapicConfigTaskFactory(), **kwargs)


class GapicConfigTaskFactory(code_gen.TaskFactoryBase):

    def get_tasks(self, **kwargs):
        return task_utils.instantiate_tasks([
            tasks.protoc.ProtoDescGenTask,
            tasks.gapic.GapicConfigGenTask,
            tasks.gapic.GapicConfigMoveTask
        ], kwargs)

    def get_validate_kwargs(self):
        return code_gen.COMMON_REQUIRED

    def get_invalid_kwargs(self):
        return ['language']


class GapicClientPipeline(code_gen.CodeGenerationPipelineBase):
    """The pipeline for generating a complete GAPIC.

    This is intended to be the only command that needs to run to generate
    a complete GAPIC.

    Exception: In Java and C#, the GrpcClientPipeline must still be
    run explicitly.
    """
    def __init__(self, language, **kwargs):
        super(GapicClientPipeline, self).__init__(
            GapicTaskFactory(),
            language=language,
            **kwargs
        )


class GapicClientBatchPipeline(batch_gen.BatchPipeline):
    def __init__(self, **kwargs):
        super(GapicClientBatchPipeline, self).__init__(
            self._make_batch_pipeline_tasks, **kwargs)

    def _make_batch_pipeline_tasks(self, **kwargs):
        task_factory = GapicTaskFactory()
        answer = task_factory.get_tasks(**kwargs)
        return task_utils.instantiate_tasks(answer, kwargs)


class GapicTaskFactory(code_gen.TaskFactoryBase):
    """A task factory describing GAPIC generation tasks.

    Language specific tasks may be defined in language-specific methods
    on this class.
    """
    def get_tasks(self, **kwargs):
        """Return the full list of instantiated tasks to generate a GAPIC.

        Args:
            kwargs (dict): Keyword arguments, which are passed through.
        """
        # Note: For languages where generating a GAPIC implies also generating
        # the GRPC or Proto library, we still generate the GAPIC _first_, even
        # though the GRPC is the dependency. This is because in some languages,
        # the GRPC is "tucked into" the GAPIC, and that process is much easier
        # if the code is generated in this order.
        answer = self._get_gapic_codegen_tasks(**kwargs)
        for grpc_task in self._get_grpc_codegen_tasks(**kwargs):
            if grpc_task not in answer:
                answer.append(grpc_task)
        answer += self._get_gapic_publish_tasks(**kwargs)
        return task_utils.instantiate_tasks(answer, kwargs)

    def _get_gapic_codegen_tasks(self, language, **kwargs):
        """Return the code generation tasks necessary for creating a GAPIC.

        Args:
            language (str): The language.

        Returns:
            list: A list of Task subclasses.
        """
        return [
            tasks.protoc.ProtoDescGenTask,
            tasks.package_metadata.PackageMetadataConfigGenTask,
            tasks.gapic.GapicCodeGenTask,
            tasks.format.get_format_task(language),
        ]

    def _get_gapic_publish_tasks(self, publish, **kwargs):
        """Dynamically import publisher tasks based on the selected publisher.

        This will raise ImportError if the publisher does not have a module
        in `pipeline.tasks.publish`.

        Args:
            publish (str): A string of a publisher in pipeline.tasks.publish.*.

        Returns:
            list: A list of Task subclasses defined by the publisher module.
        """
        module = importlib.import_module(
            'artman.tasks.publish.{}'.format(publish),
        )
        return module.TASKS

    def _get_grpc_codegen_tasks(self, language, **kw):
        """Return the code generation tasks for making a GRPC package.

        Args:
            language (str): The language code is being generated in.
            kw (dict): Additional keyword arguments passed through to the
                grpc codegen task factory.

        Returns:
            list: A list of Task subclasses defined by the GRPC task factory.
        """
        # Sanity check: Java and C# currently have an unusual workflow and
        # still must generate the grpc and gapic packages separately.
        if language in ('java', 'csharp'):
            return []

        # Instantiate the GRPC task factory.
        grpc_factory = grpc_gen._GRPC_TASK_FACTORY_DICT[language]()
        return grpc_factory._get_grpc_codegen_tasks(language=language, **kw)

    def get_validate_kwargs(self):
        return _GAPIC_REQUIRED + code_gen.COMMON_REQUIRED

    def get_invalid_kwargs(self):
        return []
