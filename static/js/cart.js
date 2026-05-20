document.addEventListener("DOMContentLoaded", function() {
  const quantityDropdown = document.querySelector(".quantity-dropdown");
  const priceElement = document.querySelector(".price");
  const totalElement = document.querySelector(".total");
  const subtotalElement = document.querySelector(".subtotal-price");
  const deliveryElement = document.querySelector(".delivery-price");
  const discountElement = document.querySelector(".discount-price");
  const totalCartElement = document.querySelector(".total-price");

  const price = parseFloat(priceElement.textContent.replace("₹", ""));

  // Retrieve selected quantity from local storage or default to 100
  let selectedQuantity = parseInt(localStorage.getItem("selectedQuantity")) || 100;
  quantityDropdown.value = selectedQuantity;

  quantityDropdown.addEventListener("change", function() {
      selectedQuantity = parseInt(quantityDropdown.value);
      localStorage.setItem("selectedQuantity", selectedQuantity); // Update local storage
      updateProductTotal();
      updateCartTotals();
  });

  function updateProductTotal() {
      const total = selectedQuantity * price;
      totalElement.textContent = "₹" + total.toFixed(2);
  }

  function updateCartTotals() {
      // Calculate the subtotal
      const subtotal = parseFloat(totalElement.textContent.replace("₹", ""));
      subtotalElement.textContent = "₹" + subtotal.toFixed(2);

      // Update the "Cart Totals" section
      const delivery = 0; // Update delivery cost as needed
      const discount = 0; // Update discount as needed

      deliveryElement.textContent = "₹" + delivery.toFixed(2);
      discountElement.textContent = "₹" + discount.toFixed(2);

      const totalCart = subtotal + delivery - discount;
      totalCartElement.textContent = "₹" + totalCart.toFixed(2);

      totalLabel.textContent = "Total:";
  }

  // Call updateProductTotal initially to set the product total based on the initial quantity
  updateProductTotal();
  // Call updateCartTotals initially to set the cart totals based on the initial quantity
  updateCartTotals();
});
