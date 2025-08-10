(function () {
  "use strict";

  // ----- DOM -----
  const canvas = document.getElementById("game");
  const ctx = canvas.getContext("2d");
  const scoreEl = document.getElementById("score");
  const highScoreEl = document.getElementById("highScore");
  const overlay = document.getElementById("overlay");
  const overlayTitle = document.getElementById("overlayTitle");
  const overlaySubtitle = document.getElementById("overlaySubtitle");
  const restartBtn = document.getElementById("restartBtn");

  // ----- Config -----
  const GRID_SIZE = 20; // количество клеток по стороне
  const INITIAL_SPEED_CELLS_PER_SEC = 8; // стартовая скорость
  const MAX_SPEED_CELLS_PER_SEC = 18;
  const SPEED_UP_EVERY_FOOD = 4; // ускорение при каждом N-ом фрукте
  const SPEED_STEP = 1; // на сколько повышать скорость

  // Цвета
  const COLOR_BG_GRID = "#111634";
  const COLOR_GRID_LINE = "#1a2146";
  const COLOR_SNAKE = "#60f0a6";
  const COLOR_SNAKE_HEAD = "#9af7c9";
  const COLOR_FOOD = "#ff6e9a";

  // ----- State -----
  /** @type {{x:number,y:number}[]} */
  let snakeCells = [];
  /** @type {{x:number,y:number}} */
  let direction = { x: 1, y: 0 };
  /** @type {{x:number,y:number}} */
  let pendingDirection = { x: 1, y: 0 };
  /** @type {{x:number,y:number}} */
  let foodCell = { x: 5, y: 5 };

  let score = 0;
  let highScore = Number(localStorage.getItem("snakeHighScoreV1") || 0);
  let isPaused = false;
  let isGameOver = false;

  // тайминг через requestAnimationFrame с фиксированным шагом обновления
  let lastTimeMs = 0;
  let accumulatorMs = 0;
  let speedCellsPerSec = INITIAL_SPEED_CELLS_PER_SEC;

  // вычисляемый размер клетки
  let cellSizePx = Math.floor(canvas.width / GRID_SIZE);

  // ----- Init -----
  function initializeGame() {
    score = 0;
    speedCellsPerSec = INITIAL_SPEED_CELLS_PER_SEC;
    isPaused = false;
    isGameOver = false;

    const startX = Math.floor(GRID_SIZE / 2);
    const startY = Math.floor(GRID_SIZE / 2);
    snakeCells = [
      { x: startX, y: startY },
      { x: startX - 1, y: startY },
      { x: startX - 2, y: startY },
    ];
    direction = { x: 1, y: 0 };
    pendingDirection = { x: 1, y: 0 };

    placeFood();
    updateScoreUI();
    hideOverlay();
  }

  function updateScoreUI() {
    scoreEl.textContent = String(score);
    highScoreEl.textContent = String(highScore);
  }

  function resizeCanvas() {
    const cssSize = Math.min(window.innerWidth * 0.88, 640);
    const dpr = Math.max(1, Math.floor(window.devicePixelRatio || 1));
    canvas.style.width = `${cssSize}px`;
    canvas.style.height = `${cssSize}px`;
    canvas.width = Math.floor(cssSize * dpr);
    canvas.height = Math.floor(cssSize * dpr);
    cellSizePx = Math.floor(canvas.width / GRID_SIZE);
  }

  function showOverlay(title, subtitle, withRestart) {
    overlayTitle.textContent = title;
    overlaySubtitle.textContent = subtitle;
    restartBtn.classList.toggle("hidden", !withRestart);
    overlay.classList.remove("hidden");
  }

  function hideOverlay() {
    overlay.classList.add("hidden");
  }

  function placeFood() {
    const occupied = new Set(snakeCells.map((c) => `${c.x}:${c.y}`));
    let attempts = 0;
    while (attempts < 1000) {
      const x = Math.floor(Math.random() * GRID_SIZE);
      const y = Math.floor(Math.random() * GRID_SIZE);
      const key = `${x}:${y}`;
      if (!occupied.has(key)) {
        foodCell = { x, y };
        return;
      }
      attempts += 1;
    }
    // fallback (змейка почти заполнила поле) — просто оставим текущую еду
  }

  // ----- Input -----
  function handleDirectionInput(next) {
    // запрет разворота на 180°
    const isOpposite = next.x + direction.x === 0 && next.y + direction.y === 0;
    if (isOpposite) return;
    pendingDirection = next;
  }

  window.addEventListener("keydown", (e) => {
    const key = e.key.toLowerCase();
    if (["arrowup", "arrowdown", "arrowleft", "arrowright", " ", "w", "a", "s", "d", "r"].includes(key)) {
      e.preventDefault();
    }

    if (key === "r") {
      initializeGame();
      return;
    }
    if (key === " ") {
      if (isGameOver) {
        initializeGame();
      } else {
        isPaused = !isPaused;
        if (isPaused) {
          showOverlay("Пауза", "Нажмите Пробел, чтобы продолжить", false);
        } else {
          hideOverlay();
        }
      }
      return;
    }

    if (key === "arrowup" || key === "w") handleDirectionInput({ x: 0, y: -1 });
    else if (key === "arrowdown" || key === "s") handleDirectionInput({ x: 0, y: 1 });
    else if (key === "arrowleft" || key === "a") handleDirectionInput({ x: -1, y: 0 });
    else if (key === "arrowright" || key === "d") handleDirectionInput({ x: 1, y: 0 });
  });

  // Touch / on-screen buttons
  document.querySelectorAll(".dpad [data-dir]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const dir = btn.getAttribute("data-dir");
      if (dir === "up") handleDirectionInput({ x: 0, y: -1 });
      if (dir === "down") handleDirectionInput({ x: 0, y: 1 });
      if (dir === "left") handleDirectionInput({ x: -1, y: 0 });
      if (dir === "right") handleDirectionInput({ x: 1, y: 0 });
    });
  });

  restartBtn.addEventListener("click", () => initializeGame());
  window.addEventListener("resize", resizeCanvas);

  // ----- Game Loop -----
  function gameLoop(timestampMs) {
    if (!lastTimeMs) lastTimeMs = timestampMs;
    const deltaMs = timestampMs - lastTimeMs;
    lastTimeMs = timestampMs;

    if (!isPaused && !isGameOver) {
      accumulatorMs += deltaMs;
      const stepMs = 1000 / speedCellsPerSec;
      while (accumulatorMs >= stepMs) {
        update();
        accumulatorMs -= stepMs;
      }
    }

    draw();
    requestAnimationFrame(gameLoop);
  }

  function update() {
    // применяем отложенное направление перед шагом
    direction = pendingDirection;

    const head = snakeCells[0];
    const nextHead = { x: head.x + direction.x, y: head.y + direction.y };

    // столкновения со стеной
    if (
      nextHead.x < 0 ||
      nextHead.y < 0 ||
      nextHead.x >= GRID_SIZE ||
      nextHead.y >= GRID_SIZE
    ) {
      return endGame();
    }

    // столкновения с собой
    for (let i = 0; i < snakeCells.length; i += 1) {
      const c = snakeCells[i];
      if (c.x === nextHead.x && c.y === nextHead.y) {
        return endGame();
      }
    }

    const ateFood = nextHead.x === foodCell.x && nextHead.y === foodCell.y;

    // добавляем голову
    snakeCells.unshift(nextHead);
    // если не съели еду — убираем хвост
    if (!ateFood) {
      snakeCells.pop();
    }

    if (ateFood) {
      score += 1;
      if (score > highScore) {
        highScore = score;
        localStorage.setItem("snakeHighScoreV1", String(highScore));
      }
      updateScoreUI();
      placeFood();

      // ускоряемся каждые N фруктов, до потолка
      if (score % SPEED_UP_EVERY_FOOD === 0) {
        speedCellsPerSec = Math.min(MAX_SPEED_CELLS_PER_SEC, speedCellsPerSec + SPEED_STEP);
      }
    }
  }

  function endGame() {
    isGameOver = true;
    showOverlay("Игра окончена", "Нажмите R или кнопку ниже, чтобы сыграть снова", true);
  }

  // ----- Rendering -----
  function draw() {
    const w = canvas.width;
    const h = canvas.height;

    // фон
    ctx.fillStyle = COLOR_BG_GRID;
    ctx.fillRect(0, 0, w, h);

    // сетка
    ctx.strokeStyle = COLOR_GRID_LINE;
    ctx.lineWidth = Math.max(1, Math.floor(cellSizePx / 12));
    ctx.beginPath();
    for (let i = 1; i < GRID_SIZE; i += 1) {
      const p = Math.floor((i * w) / GRID_SIZE) + 0.5;
      ctx.moveTo(p, 0);
      ctx.lineTo(p, h);
      ctx.moveTo(0, p);
      ctx.lineTo(w, p);
    }
    ctx.stroke();

    // еда
    drawCell(foodCell.x, foodCell.y, COLOR_FOOD, true);

    // змейка
    for (let i = snakeCells.length - 1; i >= 0; i -= 1) {
      const c = snakeCells[i];
      const isHead = i === 0;
      drawCell(c.x, c.y, isHead ? COLOR_SNAKE_HEAD : COLOR_SNAKE, false, isHead);
    }
  }

  function drawCell(x, y, color, isFood = false, isHead = false) {
    const pad = Math.max(1, Math.floor(cellSizePx * 0.12));
    const size = cellSizePx - pad * 2;
    const rx = x * cellSizePx + pad;
    const ry = y * cellSizePx + pad;

    // тень/подсветка
    if (!isFood) {
      ctx.fillStyle = "rgba(255,255,255,0.06)";
      ctx.fillRect(rx, ry + size * 0.1, size, size);
    }

    // основное тело
    ctx.fillStyle = color;
    const radius = Math.max(2, Math.floor(size * (isHead ? 0.35 : 0.28)));
    roundRect(ctx, rx, ry, size, size, radius, true, false);

    if (isHead) {
      // минимальные "глаза"
      const eye = Math.max(2, Math.floor(size * 0.08));
      const ex = rx + size * 0.25;
      const ey = ry + size * 0.25;
      ctx.fillStyle = "#091018";
      ctx.fillRect(ex, ey, eye, eye);
      ctx.fillRect(ex + size * 0.42, ey, eye, eye);
    }

    if (isFood) {
      // блик
      ctx.fillStyle = "rgba(255,255,255,0.35)";
      const b = Math.max(2, Math.floor(size * 0.18));
      roundRect(ctx, rx + b, ry + b, b * 0.9, b * 0.9, b * 0.3, true, false);
    }
  }

  function roundRect(ctx, x, y, width, height, radius, fill, stroke) {
    const r = Math.min(radius, width / 2, height / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + width, y, x + width, y + height, r);
    ctx.arcTo(x + width, y + height, x, y + height, r);
    ctx.arcTo(x, y + height, x, y, r);
    ctx.arcTo(x, y, x + width, y, r);
    ctx.closePath();
    if (fill) ctx.fill();
    if (stroke) ctx.stroke();
  }

  // ----- Start -----
  resizeCanvas();
  initializeGame();
  requestAnimationFrame(gameLoop);
})();