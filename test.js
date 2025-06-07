async function test() {
 const data = await fetch('https://btldbs-api.onrender.com/api/hoadon') 
 
 const json = await data.json()
 console.log(json) 
 const a = document.createElement('div')
 a.innerHTML = json.map(item => `<div>${item.MaDon} ${item.TongTien}</div>`).join('')
 document.body.appendChild(a)
}

test()