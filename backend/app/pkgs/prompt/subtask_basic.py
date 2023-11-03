import json
import re
import time
from app.pkgs.tools.llm import chatCompletion
from app.pkgs.tools.utils_tool import fix_llm_json_str
from app.pkgs.prompt.subtask_interface import SubtaskInterface
from app.pkgs.knowledge.app_info import getServiceSpecification
from app.pkgs.tools import storage
from config import MODE

class SubtaskBasic(SubtaskInterface):
    def splitTask(self, requirementID, feature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID, tenant_id):
        #return setpGenCode(TEST_PSEUDOCODE, feature, appBasePrompt, "- You can choose any appropriate development language", serviceStruct)
        if MODE == "FAKE":
            time.sleep(5)
            jsonData = parse_chat(FAKE_SUBTASK)
            return jsonData, True
        
        # get libs 
        data, success = setpReqChooseLib(requirementID, feature, appBasePrompt, projectInfo, projectLib)
        code_require = []
        for t in data:
            name = t['name']
            require_msg, _ = getServiceSpecification(appID, serviceName, name)
            code_require.append(require_msg)
        code_require = list(set(code_require))
        print(f"get code_require:{code_require}")
        specification = '\n'.join(code_require)
        
        # ssss
        storage.set("specification", specification)

        # subtask
        subtask, ctx, success = setpSubTask(requirementID, feature, appBasePrompt, serviceStruct, specification, serviceName)
        return subtask, success
        
    def splitTaskDo(self, req_info, service_info, tec_doc, tenant_id):
        requirement_id = req_info["requirement_id"]
        
        # ssss
        specification = storage.get("specification")
        
        service_name = service_info["name"]
        service_struct = service_info["struct_cache"]
        language = service_info["language"]
        framework = service_info["framework"]
        original_requirement = req_info["original_requirement"]

        # pseudocode
        pseudocode, success = setpPseudocode(requirement_id, language, framework, tec_doc,  service_struct, original_requirement)
        if success:
            return setpGenCode(requirement_id, pseudocode, original_requirement, specification, service_struct, service_name)
        else:
            return pseudocode, False

    def write_code(self, requirement_id, service_name, file_path, development_detail, step_id):
        pass


def setpGenCode(requirementID, pseudocode, feature, specification, serviceStruct, serviceName):
    context = []
    context.append({
        "role": "system",
        "content": """
NOTICE
Role: As a senior full stack developer, you are very diligent and good at writing complete code. 
You will get "Development specification" and "Development requirement" and "Pseudocode" for write the final complete code that works correctly.
Please note that the code should be fully functional. No placeholders no todo ensure that all code can run in production environment correctly."""})
    context.append({
        "role": "user",
        "content": """
Development specification:
```
""" + specification + """
```

Development requirement:
```
""" + feature + """
````

Pseudocode:
```
""" + pseudocode + """
```
"""})
    context.append({
        "role": "user",
        "content": """
Now complete all Pseudocode codes according to the above information including ALL code, it is going to be a long response.
Please note that the code should be fully functional. No placeholders no todo ensure that all code can run in production environment correctly.

You will output the content of each file including ALL code.
Each code file must strictly follow a markdown code block format, where the following tokens must be replaced such that
FILEPATH is a file name that contains the file extension
LANG is the markup code block language for the code's language
CODE_EXPLANATION explain the code you provide in detail, this explain should be independent. For example: specific variable names and types to be added and modified, method names to be added or modified, parameter names, and so on
CODE is the code:

filepath:FILEPATH
code explanation: CODE_EXPLANATION
```LANG
CODE```

Please note that the code should be fully functional. No placeholders.

Make sure that files contain all imports, types etc. The code should be fully functional. Make sure that code in different files are compatible with each other.
Before you finish, double check that all parts of the architecture is present in the files.
"""
    })

    # data = TEST_RESULT
    # success = True
    data, total_tokens, success = chatCompletion(context)
    
    jsonData = parse_chat(data, serviceName)
    print(jsonData)

    return jsonData, success

def setpPseudocode(requirement_id, language, framework, tec_doc,  service_struct, original_requirement):
    context = []

    content =  """
# Context
Existing Code directory structure:
```
""" + service_struct + """
```

开发需求:
```
"""+original_requirement+"""
```

将开发需求拆解为一系列必要的子步骤，并为每个步骤提供详细的说明如下：
```
""" + tec_doc + """
```
-----
作为一名资深""" + language + """系统架构师，你的任务是在""" + framework + """框架下开发。
Think step by step and reason yourself to the right decisions to make sure we get it right.

You will output the pseudocode of each file based on the "Existing Code directory structure". 
Do not write markdown code.

Each pseudocode file must strictly follow a markdown code block format, where the following tokens must be replaced such that
FILEPATH is a file name that contains the file extension
LANG is the markup code block language for the code's language
COMMENT as well as a quick comment on their purpose
CODE is the code:

FILEPATH
```LANG
# COMMENT
CODE``` 

Do not explain and talk, directly respond pseudocode of each file.
"""
    context.append({"role": "user", "content": content})
    message, total_tokens, success = chatCompletion(context)

    return message, success

def setpSubTask(requirementID, feature, appBasePrompt, serviceStruct, specification, serviceName):
    context = []
    content = """Your job is to think step by step according to the basic "Code directory structure" and "Development specification" provided below, and break down the "Development requirement" provided below into multiple substeps of writing code. each step needs to be detailed.

Only break down subtasks of writing code and do not write code, and decomposition should be appropriate and reasonable, neither over-splitting nor missing key steps.

"""+appBasePrompt+"""

Note that, Break down multiple subtasks only from the perspective of writing code. these steps should not include: "choose development language, set up environment, create directory, enexecute test, preparing the environment, execute packaging, execute deploying, write document, submit code and so on."

Code directory structure:
```
""" + serviceStruct + """
```

Development specification:
```
""" + specification + """  
```

Development requirement:
```
""" + feature + """
````

Do not explain and talk, directly respond substeps.
输出格式示例：
```
1. 在`xxx`文件中...用于...：
   - 依赖以下内容：
     - 依赖...用于..
   - 并实现以下功能：
     - ...
```
"""
    context.append({"role": "system", "content": content})
    message, total_tokens, success = chatCompletion(context)

    return message, context, success


# choose lib by req
def setpReqChooseLib(requirementID, feature, appBasePrompt, projectInfo, projectLib):
    context = []
    content = appBasePrompt + """, Your task is to analyze the requirements and find the appropriate component names. Think step by step, combine the existing project information and the existing component list, analyze the user input requirements to use which components, be careful to select only among the existing components. Please do not write code

Note that the returned component name must contain only the name but not the description. In addition, the component name must be exactly the same as that in the component list.

Service Information:
```
""" + projectInfo + """
```
    
components list:
```
""" + projectLib + """
```

requirements:
```
""" + feature + """
```
    """
    context.append({"role": "system", "content": content})
    message, total_tokens, success = chatCompletion(context)

    context.append({
        "role": "assistant",
        "content": message
    })

    context.append({
        "role": "user",
        "content": """Summary of the components chosen above.you will provide only the output in the exact format specified below with no explanation or conversation.

You should only directly respond in JSON format as described below, Ensure the response must can be parsed by Python json.loads, Response Format example:
```
[{"name":"{the name without a description}","reason":"reason","description":"description"}]
```
"""
    })

    data, total_tokens, success = chatCompletion(context)
    data = fix_llm_json_str(data)

    return json.loads(data), success

def parse_chat(chat, serviceName):
    regex = r"(.+?)```[^\n]*\n(.+?)```"
    matches = re.finditer(regex, chat, re.DOTALL)

    files = []
    for match in matches:
        print(match.group(1))
        print("=======")
        pattern = r'filepath:\s*(.*?)\s*code explanation:\s*(.*)'
        match2 = re.search(pattern, match.group(1), re.DOTALL)
        if match2:
            path = match2.group(1)
            interpreter = match2.group(2)
        else:
            path = ""
            interpreter = ""

        # Get the code
        code = match.group(2)

        # Add the file to the list
        if path.startswith(serviceName+"/"):
            path = path[len(serviceName+"/"):]
        files.append({"file-path": path,"code": code, "code-interpreter": interpreter, "reference-file": ""})

    # Return the files
    return files

FAKE_SUBTASK = """
filepath:index.html
code explanation: This is the HTML file for the game interface. It includes a canvas element for rendering the game and a link to the CSS file for styling.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Snake Game</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
    <canvas id="gameCanvas"></canvas>
    <script src="script.js"></script>
</body>
</html>
```

filepath:style.css
code explanation: This is the CSS file to style the game interface. It sets a border for the game canvas.

```css
#gameCanvas {
    border: 1px solid black;
}
```

filepath:script.js
code explanation: This is the JavaScript file to handle the game logic. It defines the Snake, Food, and Game classes, as well as event listeners for keyboard input.

```javascript
// Snake class to represent the snake in the game
class Snake {
    constructor() {
        // Initialize snake properties
        this.direction = "right";
        this.body = [
            { x: 10, y: 10 },
            { x: 9, y: 10 },
            { x: 8, y: 10 }
        ];
    }

    move() {
        // Move the snake in the current direction
        const head = { ...this.body[0] };
        switch (this.direction) {
            case "up":
                head.y--;
                break;
            case "down":
                head.y++;
                break;
            case "left":
                head.x--;
                break;
            case "right":
                head.x++;
                break;
        }
        this.body.unshift(head);
        this.body.pop();
    }

    changeDirection(direction) {
        // Change the direction of the snake
        this.direction = direction;
    }
}

// Food class to represent the food in the game
class Food {
    constructor() {
        // Initialize food properties
        this.position = { x: 5, y: 5 };
    }

    generatePosition() {
        // Generate a new random position for the food
        this.position = {
            x: Math.floor(Math.random() * 20),
            y: Math.floor(Math.random() * 20)
        };
    }
}

// Game class to manage the game state
class Game {
    constructor() {
        // Initialize game properties
        this.canvas = document.getElementById("gameCanvas");
        this.context = this.canvas.getContext("2d");
        this.snake = new Snake();
        this.food = new Food();
        this.score = 0;
        this.gameOver = false;
        this.interval = null;
    }

    start() {
        // Start the game
        this.interval = setInterval(() => {
            this.update();
            this.render();
        }, 200);
    }

    end() {
        // End the game
        clearInterval(this.interval);
        this.gameOver = true;
        alert("Game Over");
    }

    update() {
        // Update the game state
        this.snake.move();

        // Check if the snake has collided with the wall
        const head = this.snake.body[0];
        if (
            head.x < 0 ||
            head.x >= this.canvas.width / 10 ||
            head.y < 0 ||
            head.y >= this.canvas.height / 10
        ) {
            this.end();
            return;
        }

        // Check if the snake has collided with itself
        for (let i = 1; i < this.snake.body.length; i++) {
            if (head.x === this.snake.body[i].x && head.y === this.snake.body[i].y) {
                this.end();
                return;
            }
        }

        // Check if the snake has eaten the food
        if (head.x === this.food.position.x && head.y === this.food.position.y) {
            this.snake.body.push({});
            this.food.generatePosition();
            this.score++;
        }
    }

    render() {
        // Render the game on the canvas
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Render the snake
        this.context.fillStyle = "green";
        for (let i = 0; i < this.snake.body.length; i++) {
            const { x, y } = this.snake.body[i];
            this.context.fillRect(x * 10, y * 10, 10, 10);
        }

        // Render the food
        this.context.fillStyle = "red";
        const { x, y } = this.food.position;
        this.context.fillRect(x * 10, y * 10, 10, 10);

        // Render the score
        this.context.fillStyle = "black";
        this.context.font = "20px Arial";
        this.context.fillText(`Score: ${this.score}`, 10, 20);
    }
}

// Event listeners to handle keyboard input
document.addEventListener("keydown", function(event) {
    const direction = getDirection(event.keyCode);
    if (direction) {
        game.snake.changeDirection(direction);
    }
});

function getDirection(keyCode) {
    switch (keyCode) {
        case 37:
            return "left";
        case 38:
            return "up";
        case 39:
            return "right";
        case 40:
            return "down";
        default:
            return null;
    }
}

// Create an instance of the Game class
const game = new Game();

// Start the game
game.start();
```
"""


TEST_PSEUDOCODE =  """index.html
```html
<!-- The main HTML file for the game interface -->
<!DOCTYPE html>
<html>
<head>
  <title>Snake Game</title>
  <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
  <div id="game-area"></div>
  <div id="score-display"></div>
  <div id="game-over-message"></div>
  <script src="script.js"></script>
</body>
</html>
```

style.css
```css
/* CSS file to style the game interface */
#game-area {
  /* styling for the game area */
}

#score-display {
  /* styling for the score display */
}

#game-over-message {
  /* styling for the game over message */
}
```

script.js
```javascript
// JavaScript file to handle the game logic

// Function to initialize the game
function initializeGame() {
  // Code to initialize the game
}

// Function to handle keyboard input and control the snake's movement
function handleKeyboardInput(event) {
  // Code to handle keyboard input
}

// Function to generate food for the snake to eat
function generateFood() {
  // Code to generate food
}

// Function to update the snake's position based on its movement
function updateSnakePosition() {
  // Code to update the snake's position
}

// Function to check for collisions with the wall or the snake's own body
function checkCollisions() {
  // Code to check for collisions
}

// Function to handle the snake eating food and increasing its length
function handleFoodEating() {
  // Code to handle food eating
}

// Function to update the score display when the snake eats food
function updateScoreDisplay() {
  // Code to update the score display
}

// Function to end the game and display the game over message
function endGame() {
  // Code to end the game
}

// Event listener to start the game when the page loads
window.addEventListener('load', initializeGame);

// Event listener to handle keyboard input
window.addEventListener('keydown', handleKeyboardInput);"""
