# REST API Tips: PUT vs PATCH

## PUT - Complete Resource Replacement
- **Purpose**: Replace entire resource with new data
- **Behavior**: All fields must be provided, missing fields become null/default
- **Use when**: Frontend always sends complete object for updates

### Example:
```python
class ProjectRequest(BaseModel):
    project_name: str  # Required
    project_description: str  # Required

@router.put("/{project_id}")
async def update_project(project_id: str, project_data: ProjectRequest):
    # Updates ALL fields - both name and description required
    updated_project = Project(
        project_id=project_id,
        project_name=project_data.project_name,
        project_description=project_data.project_description
    )
    await repo.update(project_id, updated_project)
```

## PATCH - Partial Resource Update
- **Purpose**: Update only specific fields
- **Behavior**: Only provided fields are updated, others remain unchanged
- **Use when**: Frontend sends only changed fields

### Example:
```python
class ProjectPatchRequest(BaseModel):
    project_name: Optional[str] = None  # Optional
    project_description: Optional[str] = None  # Optional

@router.patch("/{project_id}")
async def patch_project(project_id: str, project_data: ProjectPatchRequest):
    # Updates only provided fields
    update_data = {k: v for k, v in project_data.dict().items() if v is not None}
    await repo.patch(project_id, update_data)
```

## Repository Methods

### For PUT (Complete Update):
```python
async def update(self, id: str, model: T) -> None:
    # Uses existing GenericRepository.update() method
    # Replaces all editable fields
```

### For PATCH (Partial Update):
```python
async def patch(self, id: str, partial_data: Dict[str, Any]) -> None:
    # Get existing record
    existing = await self.get_by_id(id)
    existing_dict = existing.dict()
    existing_dict.update(partial_data)  # Merge changes
    # Update with merged data
```

## Decision Guide

**Use PUT when:**
- Frontend always sends complete form data
- All fields are required for update
- You want to replace the entire editable content

**Use PATCH when:**
- Frontend sends only changed fields
- Fields are optional in update requests
- You want granular field-level updates

## Best Practice
- Be consistent across your API
- Document your choice clearly
- Consider your frontend's update patterns