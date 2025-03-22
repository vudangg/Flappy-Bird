const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.width = 400;
canvas.height = 400;

const box = 20;
let snake, food, dx, dy, gameOver, applesEaten, deaths, startTime;
let gameSpeed, gameInterval;

resetGame();

document.addEventListener("keydown", changeDirection);

function resetGame() {
    snake = [{ x: 200, y: 200, type: "x" }]; // "x" là đầu rắn
    food = { x: Math.floor(Math.random() * (canvas.width / box)) * box, y: Math.floor(Math.random() * (canvas.height / box)) * box };
    dx = box; dy = 0;
    gameOver = false;
    applesEaten = 0;
    if (deaths === undefined) deaths = 0;
    startTime = new Date();
    document.getElementById("gameOverScreen").style.display = "none";
    
    // Thiết lập tốc độ ban đầu
    gameSpeed = 100;
    
    // Xóa interval cũ nếu có
    if (gameInterval) clearInterval(gameInterval);
    
    // Tạo interval mới với tốc độ ban đầu
    gameInterval = setInterval(draw, gameSpeed);
}

// Xử lý điều khiển rắn
function changeDirection(event) {
    if (gameOver) return;
    const key = event.keyCode;
    if ((key === 37 || key === 65) && dx === 0) { dx = -box; dy = 0; }
    if ((key === 38 || key === 87) && dy === 0) { dx = 0; dy = -box; }
    if ((key === 39 || key === 68) && dx === 0) { dx = box; dy = 0; }
    if ((key === 40 || key === 83) && dy === 0) { dx = 0; dy = box; }
}

// Kiểm tra va chạm
function checkCollision() {
    for (let i = 1; i < snake.length; i++) {
        if (snake[i].x === snake[0].x && snake[i].y === snake[0].y) {
            return true; // "x" chạm "y"
        }
    }
    return false;
}

// Hàm cập nhật tốc độ game
function updateGameSpeed() {
    // Xóa interval cũ
    clearInterval(gameInterval);
    
    // Tính toán tốc độ mới (càng nhỏ càng nhanh)
    // Bắt đầu từ 100ms, mỗi táo giảm 1ms (tăng tốc độ)
    gameSpeed = Math.max(20, 100 - applesEaten);
    
    // Tạo interval mới với tốc độ đã cập nhật
    gameInterval = setInterval(draw, gameSpeed);
}

// Vẽ game
function draw() {
    if (gameOver) return;

    ctx.fillStyle = "#222";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Hiển thị thông tin
    ctx.fillStyle = "white";
    ctx.font = "16px Arial";
    ctx.fillText("Táo: " + applesEaten, 10, 20);
    ctx.fillText("Chết: " + deaths, canvas.width - 70, 20);

    let elapsedTime = Math.floor((new Date() - startTime) / 1000);
    let hours = String(Math.floor(elapsedTime / 3600)).padStart(2, "0");
    let minutes = String(Math.floor((elapsedTime % 3600) / 60)).padStart(2, "0");
    let seconds = String(elapsedTime % 60).padStart(2, "0");
    ctx.fillText(`${hours}:${minutes}:${seconds}`, canvas.width / 2 - 30, 20);

    // Vẽ thức ăn
    ctx.fillStyle = "red";
    ctx.beginPath();
    ctx.arc(food.x + box / 2, food.y + box / 2, box / 2, 0, Math.PI * 2);
    ctx.fill();

    // Vẽ rắn
    snake.forEach((part, index) => {
        ctx.beginPath();
        
        if (index === 0) {
            ctx.fillStyle = "yellow"; // Đầu rắn màu vàng (hình tam giác)

            if (dx > 0) { // Rắn đi sang phải
                ctx.moveTo(part.x, part.y);
                ctx.lineTo(part.x + box, part.y + box / 2);
                ctx.lineTo(part.x, part.y + box);
            } else if (dx < 0) { // Rắn đi sang trái
                ctx.moveTo(part.x + box, part.y);
                ctx.lineTo(part.x, part.y + box / 2);
                ctx.lineTo(part.x + box, part.y + box);
            } else if (dy > 0) { // Rắn đi xuống
                ctx.moveTo(part.x, part.y);
                ctx.lineTo(part.x + box, part.y);
                ctx.lineTo(part.x + box / 2, part.y + box);
            } else if (dy < 0) { // Rắn đi lên
                ctx.moveTo(part.x, part.y + box);
                ctx.lineTo(part.x + box, part.y + box);
                ctx.lineTo(part.x + box / 2, part.y);
            }

            ctx.fill();
        } else {
            ctx.fillStyle = "lime"; // Thân rắn giữ nguyên hình vuông
            ctx.fillRect(part.x, part.y, box, box);
        }
    });

    // Cập nhật đầu rắn
    const newHead = { x: snake[0].x + dx, y: snake[0].y + dy, type: "x" };

    // Kiểm tra va chạm
    if (newHead.x < 0 || newHead.y < 0 || newHead.x >= canvas.width || newHead.y >= canvas.height || checkCollision()) {
        deaths++;
        showGameOverScreen();
        return;
    }

    snake.unshift(newHead);
    
    if (newHead.x === food.x && newHead.y === food.y) {
        applesEaten++;
        food = { x: Math.floor(Math.random() * (canvas.width / box)) * box, y: Math.floor(Math.random() * (canvas.height / box)) * box };
        // Cập nhật tốc độ sau khi ăn táo
        updateGameSpeed();
    } else {
        snake.pop();
    }
}

// Hiển thị thông báo thua
function showGameOverScreen() {
    gameOver = true;
    let elapsedTime = Math.floor((new Date() - startTime) / 1000);
    let hours = String(Math.floor(elapsedTime / 3600)).padStart(2, "0");
    let minutes = String(Math.floor((elapsedTime % 3600) / 60)).padStart(2, "0");
    let seconds = String(elapsedTime % 60).padStart(2, "0");

    document.getElementById("appleCount").textContent = applesEaten;
    document.getElementById("playTime").textContent = `${hours}:${minutes}:${seconds}`;
    document.getElementById("gameOverScreen").style.display = "block";
}

// Không cần setInterval ở cuối nữa vì chúng ta đã quản lý nó trong resetGame
// 23/03/2025
