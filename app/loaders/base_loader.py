import os
import pandas as pd
from sqlalchemy.orm import Session
from app.core.logger import logger
from pydantic import BaseModel

def load_csv_generic(session: Session, csv_path: str, model_class, schema_class: type[BaseModel], validator=None, has_header = False):
    if not os.path.exists(csv_path):
        logger.error(f"CSV file not found: {csv_path}")
        return

    expected_columns = list(schema_class.model_fields.keys())

    try:
        df = pd.read_csv(csv_path)
        if set(df.columns) != set(expected_columns):
            logger.warning(f"CSV columns do not match schema. Assuming no header.")
            df = pd.read_csv(csv_path, header=None)
            df.columns = expected_columns
        else:
            logger.info(f"Header detected and matches schema fields.")

    except Exception as e:
        logger.error(f"Failed to read CSV at {csv_path}: {e}")
        return

    errors = []
    inserted = 0

    pk_column = list(model_class.__mapper__.primary_key)[0].name
    if pk_column in df.columns:
        duplicate_ids = df[pk_column][df[pk_column].duplicated()].unique()
        if len(duplicate_ids) > 0:
            logger.warning(
                f"Found {len(duplicate_ids)} duplicated values in column '{pk_column}' in file '{csv_path}': {duplicate_ids.tolist()}"
            )

    for idx, row in df.iterrows():
        try:
            if validator:
                validator(row)

            validated = schema_class(**row.to_dict())
            obj = model_class(**validated.model_dump())
            session.merge(obj)
            inserted += 1

        except Exception as e:
            errors.append((row.get(pk_column, f"row {idx + 1}"), str(e)))

    session.commit()
    logger.info(f"Processed {inserted} valid records into {model_class.__name__}")

    if errors:
        logger.warning(f"{len(errors)} invalid records found:")
        for err in errors:
            logger.warning(err)
