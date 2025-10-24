# Evaluate Component

Organization: Example

Organization Description: Simple example component that appends text to a JSON message file and writes a new artifact.

Version information: 0.1.0

Test status: Manual tests

Owners information:
 - You

## Usage

Load the component with:

```python
import kfp.dsl as dsl
import kfp
from kfp import components

# Local file in notebook or pipeline code
eval_op = components.load_component_from_file('components/evaluate/component.yaml')

@dsl.pipeline(name='Evaluate Pipeline')
def pipeline():
    eval_task = eval_op(
        input_message_path='artifacts/message.json',
        append_text=' - evaluated',
    )
```

### Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| input_message_path |  | Path to the input JSON file with a `message` field. |
| append_text | ` - evaluated` | Text to append to the message. |

### Outputs
- Output parameter `Updated Message Path` holds the path to the new file.
- A copy is also written to `artifacts/evaluated_message.json` for Elyra notebook steps.

### Build and Push

```bash
IMAGE=ghcr.io/your-org/evaluate-component:0.1.0
# Build context is the evaluate directory to follow this repo layout
docker build -t "$IMAGE" -f components/evaluate/Dockerfile components/evaluate

docker push "$IMAGE"
```
