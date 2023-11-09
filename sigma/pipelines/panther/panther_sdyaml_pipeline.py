import logging
from os import path
from typing import Any
from sigma.pipelines.common import logsource_windows_process_creation
from sigma.processing.pipeline import ProcessingItem, ProcessingPipeline
from sigma.processing.transformations import FieldMappingTransformation
from sigma.processing.postprocessing import QueryPostprocessingTransformation
from sigma.rule import SigmaRule

WINDOWS = "windows"
PROCESS_CREATION = "process_creation"

MAPPING = {(WINDOWS, PROCESS_CREATION): "Windows.EventLogs"}


class SdYamlTransformation(QueryPostprocessingTransformation):
    identifier = "SDYaml"

    def apply(self, pipeline: ProcessingPipeline, rule: SigmaRule, query: Any) -> Any:
        res = {
            "AnalysisType": "rule",
            "RuleID": str(rule.id),
            "DisplayName": rule.title,
            "Description": rule.description,
            "Tags": [tag.name for tag in rule.tags],
            "Enabled": True,
            "Detection": [query],
        }
        if rule.source:
            res["SigmaFile"] = path.split(rule.source.path)[-1]

        if rule.level:
            res["Severity"] = rule.level.name

        key = (rule.logsource.product, rule.logsource.category)
        log_type = MAPPING.get(key)
        if log_type is None:
            logging.error(f"Can't find LogTypes mapping for {key}")
        else:
            res["LogTypes"] = [log_type]

        return res, True


def panther_sdyaml_pipeline():
    return ProcessingPipeline(
        name="Generic Log Sources to Panther Transformation",
        # Set of identifiers of backends (from the backends mapping) that are allowed to use this processing pipeline.
        #   This can be used by frontends like Sigma CLI to warn the user about inappropriate usage.
        # allowed_backends=frozenset(),
        # The priority defines the order pipelines are applied. See documentation for common values.
        # priority=20,
        items=[
            ProcessingItem(
                transformation=FieldMappingTransformation(
                    {
                        "CommandLine": "ExtraEventData.command_line",
                        "Image": "ExtraEventData.image",
                        "ParentCommandLine": "ExtraEventData.parent_command_line",
                        "ParentImage": "ExtraEventData.parent_image",
                    }
                ),
                rule_conditions=[
                    logsource_windows_process_creation(),
                ],
            ),
        ],
        postprocessing_items=[
            SdYamlTransformation(),
        ]
    )
