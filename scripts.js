// document.addEventListener("DOMContentLoaded", () => {
//     const loader = document.getElementById("loader")
//     const categoriesContainer = document.getElementById("categories")
//     const petsContainer = document.getElementById("pets")
  
//     // Simulating loading time
//     setTimeout(() => {
//       loader.style.opacity = "0"
//       setTimeout(() => (loader.style.display = "none"), 500)
//     }, 1000)
  
//     // Sample data (replace with actual data from your backend)
//     const categories = [
//       { name: "Dogs", image: "https://via.placeholder.com/300x200.png?text=Dogs" },
//       { name: "Cats", image: "https://via.placeholder.com/300x200.png?text=Cats" },
//       { name: "Birds", image: "https://via.placeholder.com/300x200.png?text=Birds" },
//       { name: "Small Pets", image: "https://via.placeholder.com/300x200.png?text=Small+Pets" },
//     ]
  
//     const pets = [
//       { name: "Buddy", species: "Dog", image: "https://via.placeholder.com/300x200.png?text=Buddy" },
//       { name: "Whiskers", species: "Cat", image: "https://via.placeholder.com/300x200.png?text=Whiskers" },
//       { name: "Tweety", species: "Bird", image: "https://via.placeholder.com/300x200.png?text=Tweety" },
//       { name: "Hammy", species: "Hamster", image: "https://via.placeholder.com/300x200.png?text=Hammy" },
//     ]
  
//     // Render categories
//     categories.forEach((category, index) => {
//       const categoryCard = document.createElement("div")
//       categoryCard.className = "col-md-3 mb-4 fade-in"
//       categoryCard.style.animationDelay = `${index * 0.1}s`
//       categoryCard.innerHTML = `
//               <div class="card category-card">
//                   <img src="${category.image}" class="card-img-top" alt="${category.name}">
//                   <div class="card-body">
//                       <h5 class="card-title">${category.name}</h5>
//                   </div>
//               </div>
//           `
//       categoriesContainer.appendChild(categoryCard)
//     })
  
//     // Render pets
//     pets.forEach((pet, index) => {
//       const petCard = document.createElement("div")
//       petCard.className = "col-md-3 mb-4 fade-in"
//       petCard.style.animationDelay = `${index * 0.1}s`
//       petCard.innerHTML = `
//               <div class="card pet-card">
//                   <img src="${pet.image}" class="card-img-top" alt="${pet.name}">
//                   <div class="card-body">
//                       <h5 class="card-title">${pet.name}</h5>
//                       <p class="card-text">${pet.species}</p>
//                   </div>
//               </div>
//           `
//       petsContainer.appendChild(petCard)
//     })
//   })
  
  