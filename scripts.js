/* async function getSurvivors() {
    const response = await fetch("/api/survivors/");
    const data = await response.json();
  
    const survivorList = document.getElementById("survivor-list");
    survivorList.innerHTML = "";
  
    data.forEach((survivor) => {
      const listItem = document.createElement("li");
      listItem.textContent = `${survivor.name} - Age: ${survivor.age}, Gender: ${survivor.gender}, Latitude: ${survivor.latitude}, Longitude: ${survivor.longitude}`;
      survivorList.appendChild(listItem);
    });
  } */


  function getSurvivors() {
    fetch("http://localhost:8000/api/survivors/")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch survivors");
        }
        return response.json();
      })
      .then((data) => {
        displaySurvivors(data);
      })
      .catch((error) => {
        console.error(error);
      });
  }
  document.getElementById("survivor-form").addEventListener("submit", function(event) {
    event.preventDefault();
    createSurvivor();
});
  
  async function createSurvivor(event) {
    event.preventDefault();
  
    const name = document.getElementById("name").value;
    const age = parseInt(document.getElementById("age").value, 10);
    const gender = document.getElementById("gender").value;
    const latitude = parseFloat(document.getElementById("latitude").value);
    const longitude = parseFloat(document.getElementById("longitude").value);
    const water = parseInt(document.getElementById("water").value, 10);
    const food = parseInt(document.getElementById("food").value, 10);
    const medication = parseInt(document.getElementById("medication").value, 10);
    const ammunition = parseInt(document.getElementById("ammunition").value, 10);
  
    const survivorData = {
      name: name,
      age: age,
      gender: gender,
      latitude: latitude,
      longitude: longitude,
    };
  
    const itemsData = [
      { name: "water", points: 4, quantity: water },
      { name: "food", points: 3, quantity: food },
      { name: "medication", points: 2, quantity: medication },
      { name: "ammunition", points: 1, quantity: ammunition },
    ];
  
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ survivor: survivorData, items: itemsData }),
    };
  
    //const response = await fetch("/api/survivors/", requestOptions);
    const response = await fetch("http://localhost:8000/api/survivors/", requestOptions);
    const data = await response.json();
  
    if (response.status === 201) {
      alert("Survivor created successfully!");
      document.getElementById("survivor-form").reset();
      await getSurvivors();
    } else {
      alert(`Error: ${data.error}`);

      
    }
    const list = document.getElementById("list");
    const listItem = document.createElement("li");
    listItem.textContent = `${name} - ${age} - ${gender} - ${latitude}, ${longitude}`;
    list.appendChild(listItem);
  }

/*   function displaySurvivors(survivors) {
    survivorsList.innerHTML = "";
    survivors.forEach((survivor) => {
      const li = document.createElement("li");
      li.textContent = `ID: ${survivor.id}, Name: ${survivor.name}, Items: { Water: ${survivor.inventory.water}, Food: ${survivor.inventory.food}, Medication: ${survivor.inventory.medication}, Ammunition: ${survivor.inventory.ammunition} }`;
      survivorsList.appendChild(li);
    });
  } */
  function displaySurvivors(survivors) {
    const survivorsList = document.getElementById("survivors-list");
    survivorsList.innerHTML = "";
    survivors.forEach((survivor) => {
      const li = document.createElement("li");
      li.textContent = `ID: ${survivor.id}, Name: ${survivor.name}, Items: { Water: ${survivor.inventory.water.quantity}, Food: ${survivor.inventory.food.quantity}, Medication: ${survivor.inventory.medication.quantity}, Ammunition: ${survivor.inventory.ammunition.quantity} }`;
      survivorsList.appendChild(li);
    });
  }
  
  async function tradeItems(event) {
    event.preventDefault();
  
    const trader1 = parseInt(document.getElementById("trader1").value, 10);
    const trader2 = parseInt(document.getElementById("trader2").value, 10);
  
/*     const items1 = {
      water: parseInt(document.getElementById("water1").value, 10),
      food: parseInt(document.getElementById("food1").value, 10),
      medication: parseInt(document.getElementById("medication1").value, 10),
      ammunition: parseInt(document.getElementById("ammunition1").value, 10),
    };
  
    const items2 = {
      water: parseInt(document.getElementById("water2").value, 10),
      food: parseInt(document.getElementById("food2").value, 10),
      medication: parseInt(document.getElementById("medication2").value, 10),
      ammunition: parseInt(document.getElementById("ammunition2").value, 10),
    }; */

    const items1 = {
        water: parseInt(document.getElementById("trader1_water").value, 10),
        food: parseInt(document.getElementById("trader1_food").value, 10),
        medication: parseInt(document.getElementById("trader1_medication").value, 10),
        ammunition: parseInt(document.getElementById("trader1_ammunition").value, 10),
      };
      
      const items2 = {
        water: parseInt(document.getElementById("trader2_water").value, 10),
        food: parseInt(document.getElementById("trader2_food").value, 10),
        medication: parseInt(document.getElementById("trader2_medication").value, 10),
        ammunition: parseInt(document.getElementById("trader2_ammunition").value, 10),
      };
      
  
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        trader1: { id: trader1, items: items1 },
        trader2: { id: trader2, items: items2 },
      }),
    };
  
    //const response = await fetch("/api/trade/", requestOptions);
    const response = await fetch("http://localhost:8000/api/trade/", requestOptions);

    const data = await response.json();
    if (response.status === 200) {
        alert("Items traded successfully!");
        document.getElementById("trade-form").reset();
      } else {
        alert(`Error: ${data.error}`);
      }
    }
    
/*     document
      .getElementById("survivor-form")
      .addEventListener("submit", createSurvivor);
    
    document.getElementById("trade-form").addEventListener("submit", tradeItems);
    
    getSurvivors();   */

    document.getElementById("survivor-form").addEventListener("submit", createSurvivor);
    document.getElementById("trade-form").addEventListener("submit", tradeItems);
    getSurvivors();