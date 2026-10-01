//======================================
// HOME PAGE
//======================================

const heroImage = document.querySelector(".hero-image");

if(heroImage){

    heroImage.style.opacity="0";
    heroImage.style.transform="translateX(40px)";

    window.addEventListener("load",()=>{

        heroImage.style.transition="1s";
        heroImage.style.opacity="1";
        heroImage.style.transform="translateX(0)";

    });

}


//======================================
// PRODUCT CARD
//======================================

const productCards=document.querySelectorAll(".product-card");

productCards.forEach(card=>{

card.addEventListener("mouseenter",()=>{

card.style.transform="translateY(-10px)";

});

card.addEventListener("mouseleave",()=>{

card.style.transform="translateY(0)";

});

});


//======================================
// WHY CARD
//======================================

const whyCards=document.querySelectorAll(".why-card");

whyCards.forEach(card=>{

card.addEventListener("mouseenter",()=>{

card.style.transform="scale(1.05)";

});

card.addEventListener("mouseleave",()=>{

card.style.transform="scale(1)";

});

});


//======================================
// ABOUT PAGE
//======================================

const aboutCards=document.querySelectorAll(".mission-card,.feature-card,.team-card");

window.addEventListener("load",()=>{

aboutCards.forEach((card,index)=>{

card.style.opacity="0";
card.style.transform="translateY(40px)";

setTimeout(()=>{

card.style.transition=".6s";

card.style.opacity="1";

card.style.transform="translateY(0)";

},index*150);

});

});


//======================================
// UNDERTONE PAGE
//======================================

const undertoneCards=document.querySelectorAll(".undertone-card");

undertoneCards.forEach(card=>{

card.addEventListener("mouseenter",()=>{

card.style.transform="translateY(-10px)";
card.style.boxShadow="0 15px 30px rgba(0,0,0,.2)";

});

card.addEventListener("mouseleave",()=>{

card.style.transform="translateY(0)";
card.style.boxShadow="0 8px 20px rgba(0,0,0,.08)";

});

});

//======================================
// DETECT PAGE
//======================================

// Guna origin website ni sendiri (protokol+host+port semasa dibuka).
// app.py Flask kini serve WEBSITE ni SEKALI dengan API /predict dari
// server yang SAMA, jadi ni automatik betul sama ada dibuka di:
//   - laptop: http://127.0.0.1:5000
//   - fon (WiFi sama): http://<IP-laptop>:5000
// Tak payah tukar manual lagi.
const SERVER_URL = window.location.origin;

const analyzeBtn = document.querySelector(".analyze-btn");

if(analyzeBtn){

    const originalBtnHtml = analyzeBtn.innerHTML;

    analyzeBtn.addEventListener("click", async function(){

        const imageInput = document.getElementById("imageInput");

        if(imageInput.files.length === 0){

            alert("Please upload an image first.");
            return;

        }

        // UI loading state
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';

        const formData = new FormData();
        formData.append("image", imageInput.files[0]);

        try {

            const response = await fetch(`${SERVER_URL}/predict`, {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if(!response.ok || data.error){

                alert(data.error || "Gagal memproses gambar. Sila cuba gambar lain.");
                analyzeBtn.disabled = false;
                analyzeBtn.innerHTML = originalBtnHtml;
                return;

            }

            // Paparkan result terus dalam page yang sama (tanpa tukar page)
            renderResult(data);

            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = originalBtnHtml;

            document.getElementById("result").scrollIntoView({ behavior: "smooth" });

        } catch (err) {

            console.error(err);
            alert("Tak dapat hubungi server AI. Pastikan backend (python app.py) sedang berjalan.");
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = originalBtnHtml;

        }

    });

}


//======================================
// CONTACT PAGE
//======================================

const contactForm = document.getElementById("contactForm");

if(contactForm){

    contactForm.addEventListener("submit", function(e){

        e.preventDefault();

        const name = document.querySelector('input[type="text"]').value.trim();

        const email = document.querySelector('input[type="email"]').value.trim();

        const subject = document.querySelectorAll('input[type="text"]')[1].value.trim();

        const message = document.querySelector("textarea").value.trim();

        if(name === ""){
            alert("Please enter your name.");
            return;
        }

        if(email === ""){
            alert("Please enter your email.");
            return;
        }

        if(!email.endsWith("@gmail.com")){
            alert("Please enter a valid Gmail address.");
            return;
        }

        if(subject === ""){
            alert("Please enter the subject.");
            return;
        }

        if(message === ""){
            alert("Please enter your message.");
            return;
        }

        alert("Thank you for contacting BrownSkin!");

        contactForm.reset();

    });

}

//======================================
// RESULT PAGE (data SEBENAR dari AI backend)
//======================================

const undertoneColors = {
    "cool": "#2563EB",
    "warm": "#D97706",
    "neutral": "#8B5E3C",
    "olive": "#6B8E23"
};

// Cuba beberapa kemungkinan path gambar (sebab nama fail tak
// konsisten), guna yang pertama jumpa. Kalau semua gagal, guna fallback.
function setImageWithFallback(imgElement, candidatePaths, fallbackPath){
    let i = 0;
    function tryNext(){
        if(i >= candidatePaths.length){
            imgElement.src = fallbackPath;
            return;
        }
        imgElement.onerror = function(){
            i++;
            tryNext();
        };
        imgElement.src = candidatePaths[i];
    }
    tryNext();
}

function renderResult(data){

    const undertoneKey = (data.undertone || "").toLowerCase();

    // Gambar yang dimuat naik
    const uploaded = document.getElementById("uploadedImage");
    const preview = document.getElementById("previewImage");
    if(uploaded && preview){
        uploaded.src = preview.src;
    }

    // Undertone badge
    const badge = document.getElementById("undertoneBadge");
    badge.innerHTML = data.undertone.toUpperCase() + " UNDERTONE";
    badge.style.color = undertoneColors[undertoneKey] || "#333";

    // Deskripsi (skintone + confidence)
    document.getElementById("undertoneDesc").innerHTML =
        `Your Skintone: <b>${data.skintone}</b> &nbsp;|&nbsp; Confidence: <b>${data.confidence}%</b>`;

    // Foundation recommendation
    if(data.recommendations && data.recommendations.length > 0){
        const f = data.recommendations[0];
        document.getElementById("foundationShade").innerHTML = f.shade;
        document.getElementById("foundationSkintone").innerHTML = `Skintone: ${f.skintone}`;

        const shade = f.shade.toLowerCase();
        setImageWithFallback(
            document.getElementById("foundationImg"),
            [
                `shade foundation/${shade}.png`,
                `shade foundation/foundation ${shade}.png`
            ],
            "foundation brownskin.png"
        );
    } else {
        document.getElementById("foundationShade").innerHTML = "Tiada cadangan dijumpai";
        document.getElementById("foundationSkintone").innerHTML = "";
    }

    // Lipstick recommendation
    if(data.lipstick_recommendations && data.lipstick_recommendations.length > 0){
        const l = data.lipstick_recommendations[0];
        document.getElementById("lipstickShade").innerHTML = l.shade;
        document.getElementById("lipstickSkintone").innerHTML = `Skintone: ${l.skintone}`;

        const lshade = l.shade.toLowerCase();
        setImageWithFallback(
            document.getElementById("lipstickImg"),
            [
                `shade lipstick/${lshade}.png`,
                `shade lipstick/lipstick ${lshade}.png`
            ],
            "lipstik home.png"
        );
    } else {
        document.getElementById("lipstickShade").innerHTML = "Tiada cadangan dijumpai";
        document.getElementById("lipstickSkintone").innerHTML = "";
    }

}


const againBtn=document.querySelector(".again-btn");

if(againBtn){

againBtn.addEventListener("click",()=>{

document.getElementById("detect").scrollIntoView({behavior:"smooth"});

});

}

//======================================
// IMAGE PREVIEW
//======================================

const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");

if(imageInput){

    imageInput.addEventListener("change", function(){

        const file = this.files[0];

        if(file){

            const reader = new FileReader();

            reader.onload = function(e){

            previewImage.src = e.target.result;

}

            reader.readAsDataURL(file);

        }

    });

}