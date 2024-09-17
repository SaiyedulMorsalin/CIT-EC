const imgContainer = document.getElementById("img");
const addToCart = document.getElementById("add-to-cart");
addToCart.style.display = "none"
const onCursorImg = () => {
    const pdCartReview = document.getElementById("pd-cart-review");
    pdCartReview.style.display="none";
    addToCart.style.display = "block"
    console.log('mouse in');
}

const outCursorImg = () => {

    addToCart.style.display = "none";
    const pdCartReview = document.getElementById("pd-cart-review");
    pdCartReview.style.display="block";
}

