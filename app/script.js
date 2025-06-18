// script.js

document.getElementById("queryForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const from = document.getElementById("from").value.trim();
  const to = document.getElementById("to").value.trim();
  const date = document.getElementById("date").value;
  const startTime = document.getElementById("startTime").value;
  const endTime = document.getElementById("endTime").value;
  const strategy = document.getElementById("strategy").value;
  const top_k = document.getElementById("top_k").value;
  const mid = document.getElementById("middle").value;

  if (!from || !to || !date) {
    alert("请填写完整的查询信息！");
    return;
  }

  const resultArea = document.getElementById("resultArea");
  resultArea.innerHTML = "<p>正在查询中，请稍候...</p>";

  try {
    const res = await fetch(`http://localhost:5000/api/search?from=${from}&to=${to}&date=${date}&startTime=${startTime}&endTime=${endTime}&strategy=${strategy}&top_k=${top_k}&middle_station=${mid}`);
    const data = await res.json();

    if (!Array.isArray(data) || data.length === 0) {
      resultArea.innerHTML = "<p class='text-danger'>未找到中转方案</p>";
      return;
    }

    resultArea.innerHTML = "";
    data.forEach((plan, index) => {

      if(index + 1 > top_k){
        return;
      } 
    
      const card = document.createElement("div");
      card.className = "card";

      const cardBody = document.createElement("div");
      cardBody.className = "card-body";

      const title = document.createElement("h5");
      title.className = "card-title";
      title.innerText = `${index + 1}号方案：${plan.from+' -> '}${plan.route.join(" -> ")}${' -> ' + plan.to}`;

      const info = document.createElement("p");
      info.className = "card-text";
      info.innerHTML = `
        总时长：${plan.total_time}分钟<br>
        发车时间：${plan.depart_time}<br>
        抵达时间：${plan.arrive_time}<br>
        中转时间：${plan.wait_time}<br>
        总票价：<strong class="text-success">￥${plan.total_price}</strong>
      `;

     if(plan.trains[0]==plan.trains[1]){
            const station = document.createElement("a");
            station.className = "middleStation";
            station.innerText = `同车换乘`;
            cardBody.appendChild(station)
        }
      

      cardBody.appendChild(title);
      cardBody.appendChild(info);
      card.appendChild(cardBody);
      resultArea.appendChild(card);
    });

  } catch (error) {
    console.error("查询失败", error);
    resultArea.innerHTML = "<p class='text-danger'>查询失败，请检查服务器是否运行。</p>";
  }
});
