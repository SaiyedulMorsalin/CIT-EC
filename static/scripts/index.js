const imgContainer = document.getElementById("img");

const onCursorImg = (event) => {
    imgContainer.innerHTML = `
        <div class="relative img w-full overflow-hidden" id="img" onmouseover="onCursorImg(event)" onmouseout="outCursorImg(event)">
    <img class="h-full w-full object-cover" src="https://d2v5dzhdg4zhx3.cloudfront.net/web-assets/images/storypages/primary/ProductShowcasesampleimages/JPEG/Product+Showcase-1.jpg" alt="Product Image">
    <button id="add-to-cart" class="w-52 bg-black text-white absolute" style="top: 90%; left: 50%; transform: translate(-50%, -50%);"><a href="#">Add to Cart</a></button>
</div>`;
}

const outCursorImg = ()=>{
    const button = document.getElementById('add-to-cart')
    if (button){
        button.remove()
    }
}



