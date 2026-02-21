// Log button clicks to backend
function logClick(action) {
  fetch("/log_action", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({action: action})
  });
}

// Search function for secret codes
function performSearch() {
  const code = document.getElementById("searchInput").value;
  fetch("/search", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({code: code})
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("searchResult").innerText = data.result;
  });
}

// Falling petals animation for apology page
if(document.getElementById("petals")){
  const canvas = document.getElementById("petals");
  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  let petals = [];
  for(let i=0;i<50;i++){
    petals.push({
      x:Math.random()*canvas.width,
      y:Math.random()*canvas.height,
      r:5+Math.random()*5,
      speed:1+Math.random()*2
    });
  }

  function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle="pink";
    petals.forEach(p=>{
      ctx.beginPath();
      ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fill();
      p.y+=p.speed;
      if(p.y>canvas.height){
        p.y=0;
        p.x=Math.random()*canvas.width;
      }
    });
  }
  setInterval(draw,30);
}

// Fireworks animation for promise page
function celebrate() {
  let canvas = document.getElementById("confetti");
  let ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  let particles = [];
  for(let i=0;i<200;i++){
    particles.push({
      x:canvas.width/2,
      y:canvas.height/2,
      vx:(Math.random()-0.5)*6,
      vy:(Math.random()-0.5)*6,
      color:`hsl(${Math.random()*360},100%,50%)`
    });
  }

  function animate(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    particles.forEach(p=>{
      ctx.fillStyle=p.color;
      ctx.beginPath();
      ctx.arc(p.x,p.y,3,0,Math.PI*2);
      ctx.fill();
      p.x+=p.vx;
      p.y+=p.vy;
      p.vy+=0.05; // gravity
    });
    requestAnimationFrame(animate);
  }
  animate();
}