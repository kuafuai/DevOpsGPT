import json
import re
import time
from app.pkgs.tools.llm import chatCompletion
from app.pkgs.tools.utils_tool import fix_llm_json_str
from app.pkgs.prompt.subtask_interface import SubtaskInterface
from app.pkgs.knowledge.app_info import getServiceSpecification, getServiceStruct
from config import MODE
from app.pkgs.tools.i18b import getCurrentLanguageName

class SubtaskBasic(SubtaskInterface):
    def splitTask(self, feature, serviceName, appBasePrompt, projectInfo, projectLib, serviceStruct, appID):
        #return setpGenCode(TEST_PSEUDOCODE, feature, appBasePrompt, "- You can choose any appropriate development language", serviceStruct)
        if MODE == "FAKE":
            time.sleep(10)
            jsonData = parse_chat(TEST_RESULT)
            return jsonData, True
        
        # get libs 
        data, success = setpReqChooseLib(feature, appBasePrompt, projectInfo, projectLib)
        code_require = []
        default_msg, _ = getServiceSpecification(appID, serviceName, "Default")
        code_require.append(default_msg)
        for t in data:
            name = t['name']
            require_msg, _ = getServiceSpecification(appID, serviceName, name)
            code_require.append(require_msg)
        code_require = list(set(code_require))
        print(f"get code_require:{code_require}")
        specification = '\n'.join(code_require)

        # subtask
        subtask, ctx, success = setpSubTask(feature, appBasePrompt, serviceStruct, specification)
        if success:
            # pseudocode
            pseudocode, success = setpPseudocode(ctx, subtask,  serviceStruct, appBasePrompt)
            if success:
                return setpGenCode(pseudocode, feature, appBasePrompt, specification, serviceStruct)
            else:
                return pseudocode, False
        else:
            return subtask, False


def setpGenCode(pseudocode, feature, appBasePrompt, specification, serviceStruct):
    context = []
    context.append({
        "role": "system",
        "content": """
NOTICE
Role: As a senior full stack developer, you are very diligent and good at writing complete code. 
You will get "Development specification" and "Development requirement" and "Pseudocode" for write the final complete code that works correctly.
Please note that the code should be fully functional. No placeholders no todo ensure that all code can run in production environment correctly.
"""+appBasePrompt+""" """})
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
Now complete all codes according to the above information including ALL code, it is going to be a long response.
Please note that the code should be fully functional. No placeholders no todo ensure that all code can run in production environment correctly.

You will output the content of each file including ALL code.
Each code file must strictly follow a markdown code block format, where the following tokens must be replaced such that
FILEPATH is the lowercase file name including the file extension
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
    data, success = chatCompletion(context)
    
    jsonData = parse_chat(data)
    print(jsonData)

    return jsonData, success

def setpPseudocode(context, subtask, serviceStruct, appBasePrompt):
    context.append({"role": "assistant", "content": subtask})

    content =  """
Think step by step and reason yourself to the right decisions to make sure we get it right.

You will output the pseudocode of each file based on the "Existing Code directory structure" provided below. 
Do not write markdown code.
"""+appBasePrompt+"""

Existing code directory structure:
```
""" + serviceStruct + """
```

Each pseudocode file must strictly follow a markdown code block format, where the following tokens must be replaced such that
FILEPATH is the lowercase file name including the file extension
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
    message, success = chatCompletion(context)

    return message, success

def setpSubTask(feature, appBasePrompt, serviceStruct, specification):
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
"""
    context.append({"role": "system", "content": content})
    message, success = chatCompletion(context)

    return message, context, success


# choose lib by req
def setpReqChooseLib(feature, appBasePrompt, projectInfo, projectLib):
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
    message, success = chatCompletion(context)

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

    data, success = chatCompletion(context)

    return json.loads(data), success

def parse_chat(chat):
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
        files.append({"file-path": path,"code": code, "code-interpreter": interpreter, "reference-file": ""})

    # Return the files
    return files

# just for test
TEST_RESULT = """filepath:index.html
code explanation: This file is the main HTML file for the game interface. It contains the structure of the game interface and includes the necessary CSS and JavaScript files.

```html
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

filepath:style.css
code explanation: This file is used to style the game interface. It contains CSS styles for the game area, score display, and game over message.

```css
#game-area {
  /* CSS styles for the game area */
}

#score-display {
  /* CSS styles for the score display */
}

#game-over-message {
  /* CSS styles for the game over message */
}
```

filepath:script.js
code explanation: This file contains the game logic. It defines variables for game elements and state, and implements functions to initialize the game, handle keyboard inputs, update the game state, render the game interface, start and end the game, restart the game, pause or resume the game, handle game over conditions, generate random food position, check for collisions, update the score display, update the snake's position and length, handle snake movement, handle snake eating food, and handle the game timer.

```javascript
// Define variables for game elements and state
let gameArea;
let scoreDisplay;
let gameOverMessage;
let snake;
let food;
let score;
let gameIsOver;
let gameTimer;

// Function to initialize the game
function initializeGame() {
  gameArea = document.getElementById('game-area');
  scoreDisplay = document.getElementById('score-display');
  gameOverMessage = document.getElementById('game-over-message');
  snake = [{ x: 0, y: 0 }];
  food = { x: 0, y: 0 };
  score = 0;
  gameIsOver = false;
  gameTimer = null;

  renderGameInterface();
  startGame();
}

// Function to handle keyboard inputs
function handleKeyboardInput(event) {
  if (event.key === 'ArrowUp' && snake[0].y !== -1) {
    snake[0].y = -1;
    snake[0].x = 0;
  } else if (event.key === 'ArrowDown' && snake[0].y !== 1) {
    snake[0].y = 1;
    snake[0].x = 0;
  } else if (event.key === 'ArrowLeft' && snake[0].x !== -1) {
    snake[0].x = -1;
    snake[0].y = 0;
  } else if (event.key === 'ArrowRight' && snake[0].x !== 1) {
    snake[0].x = 1;
    snake[0].y = 0;
  }
}

// Function to update the game state
function updateGameState() {
  updateSnake();
  handleSnakeEatingFood();
  checkCollisions();
  updateScoreDisplay();
}

// Function to render the game interface
function renderGameInterface() {
  gameArea.innerHTML = '';
  for (let y = 0; y < 20; y++) {
    for (let x = 0; x < 20; x++) {
      const cell = document.createElement('div');
      cell.classList.add('cell');
      if (x === food.x && y === food.y) {
        cell.classList.add('food');
      }
      for (const segment of snake) {
        if (segment.x === x && segment.y === y) {
          cell.classList.add('snake');
        }
      }
      gameArea.appendChild(cell);
    }
  }
  scoreDisplay.textContent = `Score: ${score}`;
  gameOverMessage.textContent = '';
}

// Function to start the game
function startGame() {
  document.addEventListener('keydown', handleKeyboardInput);
  gameTimer = setInterval(() => {
    if (!gameIsOver) {
      updateGameState();
      renderGameInterface();
    }
  }, 200);
}

// Function to end the game
function endGame() {
  gameIsOver = true;
  clearInterval(gameTimer);
  gameOverMessage.textContent = `Game Over! Final Score: ${score}`;
}

// Function to restart the game
function restartGame() {
  snake = [{ x: 0, y: 0 }];
  food = { x: 0, y: 0 };
  score = 0;
  gameIsOver = false;
  renderGameInterface();
  startGame();
}

// Function to pause or resume the game
function togglePauseGame() {
  if (gameIsOver) {
    return;
  }
  if (gameTimer) {
    clearInterval(gameTimer);
    gameTimer = null;
  } else {
    gameTimer = setInterval(() => {
      if (!gameIsOver) {
        updateGameState();
        renderGameInterface();
      }
    }, 200);
  }
}

// Function to handle game over conditions
function handleGameOver() {
  const head = snake[0];
  if (head.x < 0 || head.x >= 20 || head.y < 0 || head.y >= 20) {
    endGame();
  }
  for (let i = 1; i < snake.length; i++) {
    if (head.x === snake[i].x && head.y === snake[i].y) {
      endGame();
      break;
    }
  }
}

// Function to generate random food position
function generateFoodPosition() {
  food.x = Math.floor(Math.random() * 20);
  food.y = Math.floor(Math.random() * 20);
}

// Function to check for collisions with walls or snake body
function checkCollisions() {
  handleGameOver();
}

// Function to update the score display
function updateScoreDisplay() {
  scoreDisplay.textContent = `Score: ${score}`;
}

// Function to update the snake's position and length
function updateSnake() {
  const head = { x: snake[0].x, y: snake[0].y };
  snake.unshift(head);
  if (head.x === food.x && head.y === food.y) {
    score++;
    generateFoodPosition();
  } else {
    snake.pop();
  }
}

// Function to handle snake movement
function handleSnakeMovement() {
  const head = snake[0];
  head.x += head.x;
  head.y += head.y;
}

// Function to handle snake eating food
function handleSnakeEatingFood() {
  const head = snake[0];
  if (head.x === food.x && head.y === food.y) {
    score++;
    generateFoodPosition();
  }
}

// Function to handle game timer
function handleGameTimer() {
  if (!gameIsOver) {
    updateGameState();
    renderGameInterface();
  }
}

// Function to handle game initialization
function handleGameInitialization() {
  initializeGame();
}

// Call the function to initialize the game
handleGameInitialization();
```

Please note that the above code is a complete implementation of the Snake Game based on the provided development specification and requirements. However, it may require additional styling and fine-tuning to meet specific design preferences and performance optimizations."""


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
