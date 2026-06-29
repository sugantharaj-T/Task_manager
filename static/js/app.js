document.querySelectorAll(".kanban-card").forEach((card) => {
  card.addEventListener("mouseenter", () => card.classList.add("shadow-sm"));
  card.addEventListener("mouseleave", () => card.classList.remove("shadow-sm"));
});
