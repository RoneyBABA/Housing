// Reveal animation
const cards = document.querySelectorAll('.card');
function revealCards() {
  const trigger = window.innerHeight * 0.85;
  cards.forEach(card => {
    const top = card.getBoundingClientRect().top;
    if (top < trigger) card.classList.add('visible');
  });
}
window.addEventListener('scroll', revealCards);
revealCards();

window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  const gradient = document.querySelector('.scroll-gradient');
  gradient.style.opacity = Math.min(scrollY / 400, 1);
});

const locations = {{ locations|tojson }};
const input = document.getElementById("location");
const suggestionBox = document.getElementById("suggestions");
let selectedIndex = -1;

// Levenshtein distance function
function levenshtein(a, b) {
  const dp = Array(a.length + 1).fill().map(() => Array(b.length + 1).fill(0));
  for (let i = 0; i <= a.length; i++) dp[i][0] = i;
  for (let j = 0; j <= b.length; j++) dp[0][j] = j;

  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      dp[i][j] = Math.min(
        dp[i - 1][j] + 1,
        dp[i][j - 1] + 1,
        dp[i - 1][j - 1] + cost
      );
    }
  }
  return dp[a.length][b.length];
}

// Generate ranked suggestions
function getSuggestions(query) {
  const lowerQuery = query.toLowerCase();

  return locations
    .map(loc => {
      const lowerLoc = loc.toLowerCase();
      const startsWith = lowerLoc.startsWith(lowerQuery);
      const dist = levenshtein(lowerQuery, lowerLoc.slice(0, lowerQuery.length));
      return { loc, score: startsWith ? dist - 2 : dist }; // reward prefix matches
    })
    .sort((a, b) => a.score - b.score || a.loc.localeCompare(b.loc))
    .slice(0, 5)
    .map(m => m.loc);
}

// Render dropdown suggestions
function showSuggestions(suggestions) {
  suggestionBox.innerHTML = "";
  selectedIndex = -1;

  suggestions.forEach((sugg, index) => {
    const li = document.createElement("li");
    li.textContent = sugg;
    li.onclick = () => {
      input.value = sugg;
      suggestionBox.innerHTML = "";
    };
    suggestionBox.appendChild(li);
  });
}

// Handle input typing
input.addEventListener("input", () => {
  const query = input.value.trim();
  suggestionBox.innerHTML = "";

  if (!query) return;
  const matches = getSuggestions(query);
  showSuggestions(matches);
});

// Handle keyboard navigation
input.addEventListener("keydown", (e) => {
  const items = suggestionBox.querySelectorAll("li");

  if (e.key === "ArrowDown") {
    e.preventDefault();
    selectedIndex = (selectedIndex + 1) % items.length;
    updateSelection(items);
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    selectedIndex = (selectedIndex - 1 + items.length) % items.length;
    updateSelection(items);
  } else if (e.key === "Enter") {
    e.preventDefault();
    if (selectedIndex >= 0 && items[selectedIndex]) {
      input.value = items[selectedIndex].textContent;
      suggestionBox.innerHTML = "";
    }
  }
});

// Highlight selected item
function updateSelection(items) {
  items.forEach((item, i) => {
    item.classList.toggle("selected", i === selectedIndex);
  });
}

// Hide suggestions when clicking elsewhere
document.addEventListener("click", (e) => {
  if (!suggestionBox.contains(e.target) && e.target !== input) {
    suggestionBox.innerHTML = "";
  }
});
