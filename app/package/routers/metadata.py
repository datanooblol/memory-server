from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from package.auth.jwt_auth import verify_token
from package.data_models import Metadata, FieldMetadata
from package.routers.dependencies import get_source_repo, get_metadata_repo, get_field_metadata_repo
from pathlib import Path
from package.data_catalogs.local import DataCatalog

router = APIRouter(prefix="/metadata", tags=["metadata"])

class MetadataRequest(BaseModel):
    metadata: Metadata
    fields: list[FieldMetadata]

async def get_or_create_metadata(source_id, source_repo, metadata_repo, field_metadata_repo):
    # Check if metadata exists
    existing_metadata = await metadata_repo.find_by({"source_id": source_id})
    existing_field_metadata = await field_metadata_repo.find_by({"source_id": source_id})
    if not (existing_metadata and existing_field_metadata):
        source = await source_repo.get_by_id(source_id)
        new_metadata = Metadata(
            source_id=source_id,
            table_name=source.source_name
        )
        profile = DataCatalog.profile(Path(source.source_path["stored_path"]))
        new_field_metadata = [
            FieldMetadata(
                source_id=source_id,
                field_name=p["field_name"],
                data_type=p["data_type"]
            )
            for p in profile
        ]
        await metadata_repo.create(new_metadata)
        await field_metadata_repo.batch_create(new_field_metadata)
        existing_metadata = new_metadata
        existing_field_metadata = new_field_metadata
    else:
        # Extract first item from lists when they exist
        existing_metadata = existing_metadata[0]
    return MetadataRequest(metadata=existing_metadata, fields=existing_field_metadata)

# GET /metadata/source/{source_id} - Smart get with auto-extraction
@router.get("/source/{source_id}", response_model=MetadataRequest)
async def get_metadata(
    source_id: str,
    user_id: str = Depends(verify_token),
    source_repo = Depends(get_source_repo),
    metadata_repo = Depends(get_metadata_repo),
    field_metadata_repo = Depends(get_field_metadata_repo)
):
    records = await get_or_create_metadata(source_id, source_repo, metadata_repo, field_metadata_repo)
    return records

# PUT /metadata/{metadata_id} - Update existing metadata
@router.put("/")
async def update_metadata(
    metadata_data: MetadataRequest,
    user_id: str = Depends(verify_token),
    metadata_repo = Depends(get_metadata_repo),
    field_metadata_repo = Depends(get_field_metadata_repo)
):
    # Update metadata and field metadata
    new_metadata = metadata_data.metadata
    new_fields:list[FieldMetadata] = metadata_data.fields
    await metadata_repo.update(new_metadata.metadata_id, new_metadata)
    await field_metadata_repo.batch_update(new_fields)
    return {"message": "Metadata updated successfully"}

# DELETE /metadata/{metadata_id} - Delete metadata
@router.delete("/source/{source_id}")
async def delete_metadata(
    source_id: str,
    user_id: str = Depends(verify_token),
    metadata_repo = Depends(get_metadata_repo),
    field_metadata_repo = Depends(get_field_metadata_repo)
):
    # Delete metadata and related field metadata
    await metadata_repo.delete_by({"source_id": source_id})
    await field_metadata_repo.delete_by({"source_id": source_id})
    return {"message": "Metadata deleted successfully"}
