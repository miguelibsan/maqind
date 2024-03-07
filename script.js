function addDate() {
    const date = new Date();
    const formattedDate = date.toLocaleDateString("es-MX", {
      weekday: "long",
      day: "numeric",
      month: "long",
      year: "numeric",
    });
  
    const element = document.createElement("p");
    element.textContent = formattedDate;
    element.classList.add("date");
  
    document.querySelector("header").appendChild(element);
  }
  
  addDate();
  