#!/usr/bin/env python3
"""Minimal JSON Schema subset validator (stdlib only).

Supports: type (including unions), const, enum, required, properties,
additionalProperties, pattern, minimum, maximum, minLength, maxLength,
minItems, minProperties, items, and bool schemas.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class SchemaError(ValueError):
    pass


def load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_instance(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    _validate(instance, schema, path, errors)
    return errors


def _validate(instance: Any, schema: Any, path: str, errors: list[str]) -> None:
    if schema is True:
        return
    if schema is False:
        errors.append(f"{path}: false schema rejects all values")
        return
    if not isinstance(schema, dict):
        errors.append(f"{path}: invalid schema object")
        return

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
        return

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not in enum {schema['enum']!r}")
        return

    if "type" in schema:
        if not _type_ok(instance, schema["type"]):
            errors.append(f"{path}: expected type {schema['type']!r}, got {type(instance).__name__}")
            return

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: string shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: string longer than maxLength {schema['maxLength']}")
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            errors.append(f"{path}: string does not match pattern {schema['pattern']!r}")

    if isinstance(instance, bool):
        pass
    elif isinstance(instance, int):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: integer below minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: integer above maximum {schema['maximum']}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: array shorter than minItems {schema['minItems']}")
        item_schema = schema.get("items")
        if item_schema is not None:
            for i, item in enumerate(instance):
                _validate(item, item_schema, f"{path}[{i}]", errors)

    if isinstance(instance, dict):
        if "minProperties" in schema and len(instance) < schema["minProperties"]:
            errors.append(f"{path}: object has fewer than minProperties {schema['minProperties']}")
        required = schema.get("required") or []
        for key in required:
            if key not in instance:
                errors.append(f"{path}: missing required property {key!r}")
        props = schema.get("properties") or {}
        additional = schema.get("additionalProperties", True)
        for key, value in instance.items():
            if key in props:
                _validate(value, props[key], f"{path}.{key}", errors)
            elif additional is False:
                errors.append(f"{path}: unexpected property {key!r}")
            elif isinstance(additional, dict):
                _validate(value, additional, f"{path}.{key}", errors)


def _type_ok(instance: Any, expected: Any) -> bool:
    if isinstance(expected, list):
        return any(_type_ok(instance, t) for t in expected)
    if expected == "object":
        return isinstance(instance, dict)
    if expected == "array":
        return isinstance(instance, list)
    if expected == "string":
        return isinstance(instance, str)
    if expected == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if expected == "number":
        return (isinstance(instance, (int, float)) and not isinstance(instance, bool))
    if expected == "boolean":
        return isinstance(instance, bool)
    if expected == "null":
        return instance is None
    return False
