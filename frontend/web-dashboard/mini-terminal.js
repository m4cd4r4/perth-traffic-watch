// ============================================================================
// Mini Terminal & Modal
// ============================================================================

let miniTerminalLines = [];
const MAX_MINI_LINES = 20;

function updateMiniTerminal(html) {
  const miniOutput = document.getElementById('mini-terminal-output');
  const modalOutput = document.getElementById('modal-terminal-output');

  if (miniOutput) {
    miniOutput.insertAdjacentHTML('beforeend', html);
    miniOutput.scrollTop = miniOutput.scrollHeight;

    // Limit lines in mini terminal
    while (miniOutput.children.length > MAX_MINI_LINES) {
      miniOutput.removeChild(miniOutput.firstChild);
    }
  }

  if (modalOutput) {
    modalOutput.insertAdjacentHTML('beforeend', html);
    modalOutput.scrollTop = modalOutput.scrollHeight;

    // Limit lines in modal
    while (modalOutput.children.length > 500) {
      modalOutput.removeChild(modalOutput.firstChild);
    }
  }
}

function initMiniTerminal() {
  const expandBtn = document.getElementById('expand-terminal-btn');
  const modal = document.getElementById('terminal-modal');
  const closeBtn = document.getElementById('close-terminal-modal');

  if (expandBtn && modal) {
    expandBtn.addEventListener('click', () => {
      modal.classList.add('active');
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener('click', () => {
      modal.classList.remove('active');
    });
  }

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
      modal.classList.remove('active');
    }
  });

  // Close on backdrop click
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('active');
      }
    });
  }

  // Start the mini terminal feed
  startMiniTerminalFeed();
}

function startMiniTerminalFeed() {
  // Initial messages
  updateMiniTerminal('<div class="terminal-line">[SIM] Connected to simulator</div>');
  updateMiniTerminal('<div class="terminal-line">[SIM] Monitoring Stirling Hwy corridor</div>');

  // Generate simulated detections
  setInterval(() => {
    const sites = [
      'Mounts Bay Rd @ Kings Park',
      'Mounts Bay Rd @ Mill Point',
      'Stirling Hwy @ Eric St',
      'Stirling Hwy @ Forrest St',
      'Stirling Hwy @ Bay View'
    ];
    const site = sites[Math.floor(Math.random() * sites.length)];
    const count = Math.floor(Math.random() * 8) + 1;
    const direction = Math.random() > 0.5 ? 'NB' : 'SB';
    const confidence = (85 + Math.random() * 14).toFixed(1);

    const lineTypes = [
      '<div class="terminal-line detection">[DET] ' + site + ' (' + direction + '): ' + count + ' vehicles @ ' + confidence + '%</div>',
      '<div class="terminal-line">[SIM] ' + site + ': Speed ' + Math.floor(40 + Math.random() * 30) + ' km/h</div>'
    ];

    const line = lineTypes[Math.floor(Math.random() * lineTypes.length)];
    updateMiniTerminal(line);
  }, 800);
}

// Initialize mini terminal when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(initMiniTerminal, 1000);
});
