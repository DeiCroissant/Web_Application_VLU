let display = document.getElementById('display');
let currentInput = '0';
let operator = '';
let previousInput = '';
let waitingForOperand = false;

function updateDisplay() {
    display.textContent = currentInput;
}

function appendToDisplay(value) {
    if (waitingForOperand) {
        currentInput = value;
        waitingForOperand = false;
    } else {
        if (currentInput === '0') {
            currentInput = value;
        } else {
            currentInput += value;
        }
    }
    
    // Handle operators
    if (['+', '-', '*', '/'].includes(value)) {
        if (operator && previousInput !== '' && !waitingForOperand) {
            calculate();
        }
        
        operator = value;
        previousInput = currentInput;
        waitingForOperand = true;
    }
    
    updateDisplay();
}

function calculate() {
    if (operator && previousInput !== '' && currentInput !== '' && !waitingForOperand) {
        let prev = parseFloat(previousInput);
        let current = parseFloat(currentInput);
        let result;
        
        switch (operator) {
            case '+':
                result = prev + current;
                break;
            case '-':
                result = prev - current;
                break;
            case '*':
                result = prev * current;
                break;
            case '/':
                if (current === 0) {
                    alert('Cannot divide by zero!');
                    clearDisplay();
                    return;
                }
                result = prev / current;
                break;
            default:
                return;
        }
        
        // Round to avoid floating point precision issues
        result = Math.round(result * 100000000) / 100000000;
        
        currentInput = result.toString();
        operator = '';
        previousInput = '';
        waitingForOperand = true;
        
        updateDisplay();
    }
}

function clearDisplay() {
    currentInput = '0';
    operator = '';
    previousInput = '';
    waitingForOperand = false;
    updateDisplay();
}

function clearEntry() {
    currentInput = '0';
    updateDisplay();
}

// Handle keyboard input
document.addEventListener('keydown', function(event) {
    const key = event.key;
    
    if (key >= '0' && key <= '9') {
        appendToDisplay(key);
    } else if (key === '.') {
        if (currentInput.indexOf('.') === -1) {
            appendToDisplay(key);
        }
    } else if (['+', '-', '*', '/'].includes(key)) {
        appendToDisplay(key);
    } else if (key === 'Enter' || key === '=') {
        event.preventDefault();
        calculate();
    } else if (key === 'Escape' || key === 'c' || key === 'C') {
        clearDisplay();
    } else if (key === 'Backspace') {
        if (currentInput.length > 1) {
            currentInput = currentInput.slice(0, -1);
        } else {
            currentInput = '0';
        }
        updateDisplay();
    }
});

// Initialize display
updateDisplay();
