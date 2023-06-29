def handle_shop_resp(products, page_number: int, pages_number: int, ration_lines: str=None) -> str:
    start = """
                <!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <title>Dynamic Pagination</title>
    <style>
    *{
			padding: 0;
			margin: 0;
		}
		body{
			margin: 50px;
		}
		main{
			widows: 70%;
			height: auto;
			padding: 20px;
			margin: 50px auto;
			background: whitesmoke;
			font-family: system-ui;
			color: #666;
		}
		.header{
			width: 90%;
			height: 100px;
			margin: auto;
			display: flex;
			justify-content: space-between;
			align-items: center;
		}
		.items-controller,
		.search{
			flex-shrink: 0;
			display: flex;
			align-content: center;
			align-items: center;

		}
		select{
		 	padding: 2px;
	    	margin: 0 10px;
	   		outline: none;
	    	cursor: pointer;
	    	border: none;
	    	background: transparent;
		}
		.search > input{
			padding: 8px;
		    border: none;
		    outline: navajowhite;
		    margin: 0 0 0 20px;
		    background: white;
		}
		.field{
			width: 90%;
			height: auto;
			margin: auto;
		}
		table{
			width: 100%;
			margin: 2px auto;
			table-layout: auto;
			color: #757575;
			background-color: #ffff;
			border-collapse: collapse;
			border-spacing: 0;
			text-align: left;
		}
		table tr th, td{
			padding: 10px;
			border: 1px solid #ccc;
		}
		.bottom-field{
			width: 100%;
			padding: 20px;
			margin-top: 20px;
		}
		.pagination{
	      display: flex;
	      justify-content: center;
	      align-items: center;
	    }
	    .pagination li{
	      list-style: none;
	      padding: 2px;
	      margin: 10px;
	      flex-shrink: 0;
	      text-align: center;
	      border-radius: 5px;
	      border: 1px solid #999;
	      color: #999;
	    }
	    .pagination li.active{
	      background: #32d6aa;
	      color: white;
	      border-color: #32d6aa;

	    }
	    .pagination li a{
	      text-decoration: none;
	      padding: 3px 8px;
	      color: inherit;
	      display: block;
	      font-family: sans-serif;
	      font-size: 13px;
	    }
	    i.fa-edit{color: lime;}
		i.fa-trash{color: red;}
    </style>
</head>
<body onload="script();">

    <main>
        <section class="header">
            <div class="items-controller">
                <span name="" id="itemperpage" hidden="hidden" , value="10">
				</span>
                <input type=hidden id="shops_list" name="shops_list_name" value=""/>
            </div>
            <div class="search">
                <h5>Search</h5>
                <input type="text" name="" id="search" placeholder="search">
            </div>
        </section>
        <section class="field">
            <table border=1>
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th>Photo</th>
                                <th>Price without discount</th>
                                <th>Discounted price</th>
                                <th>Weigth</th>
                                <th>Discount</th>
                                <th>Date of production</th>
                                <th>Expiration date</th>
                            </tr>
                        </thead>
                        <tbody>
            """
    end_table = """   
                    </tbody>
			    </table>
    """
    end_beg = """		    
            <div class="bottom-field">
                <ul class="pagination">
                  <li class="prev"><a href="#" id="prev">&#139;</a></li>
                    <!-- page number here -->
                  <li class="next"><a href="#" id="next">&#155;</a></li>
                </ul>
            </div>
        </section>
    </main>
    



<script type="text/javascript">
		var tbody = document.querySelector("tbody");
		var pageUl = document.querySelector(".pagination");
		var itemShow = document.querySelector("#itemperpage");
		var tr = tbody.querySelectorAll("tr");
		var emptyBox = [];
	"""
    end_middle = """var index = """
    end_end_beg = """
            
            var itemPerPage = 10;
        //window.location.href = "https://127.0.0.1/get_page" + "?page_number=" + index + "&shops_list=['5ka']";
		for(let i=0; i<tr.length; i++){ emptyBox.push(tr[i]);}

		itemShow.onchange = giveTrPerPage;
		function giveTrPerPage(){
			itemPerPage = Number(this.value);
			// console.log(itemPerPage);
			displayPage(itemPerPage);
			pageGenerator(itemPerPage);
			getpagElement(itemPerPage);
		}

		function displayPage(limit){
			tbody.innerHTML = '';
			for(let i=0; i<limit; i++){
				tbody.appendChild(emptyBox[i]);
			}
			const  pageNum = pageUl.querySelectorAll('.list');
			pageNum.forEach(n => n.remove());
		}
		displayPage(itemPerPage);

        function clear_pages() {
            pages = document.querySelectorAll("li")
            if (pages.length > 2) {
                for (let i = 1; i < pages.length - 1; ++i) {
                    pages[i].remove()
                }
            }
        }

		function pageGenerator(getem){
			const num_of_tr = emptyBox.length;
			//if(num_of_tr <= getem){
			//	pageUl.style.display = 'none';
			//}else{
                
				pageUl.style.display = 'flex';
    """
    end_end_middle = f'const num_Of_Page = {pages_number};'
				
    end_end_end = """
                clear_pages()
                
				for(i=index; (i <= parseInt(index) + 5) && (i < num_Of_Page); i++){
					const li = document.createElement('li'); li.className = 'list';
                    if (i == index) {
						li.classList.add("active");
					}
					const a =document.createElement('a'); a.href = '#'; a.innerText = i;
					a.setAttribute('data-page', i);
					li.appendChild(a);
					pageUl.insertBefore(li,pageUl.querySelector('.next'));
				}
			//}
		}
		pageGenerator(itemPerPage);
		let pageLink = pageUl.querySelectorAll("a");
		let lastPage =  pageLink.length - 2;
		
		function pageRunner(page, items, lastPage, active){
			for(button of page){
				button.onclick = e=>{
					const page_num = e.target.getAttribute('data-page');
					const page_mover = e.target.getAttribute('id');
					if(page_num != null){
						index = page_num;
					}else{
						if(page_mover === "next"){
							index++;
							if(index >= lastPage){
								index = lastPage;
							}
						}else{
							index--;
							if(index <= 1){
								index = 1;
							}
						}
                        
					}
                    pageGenerator(itemPerPage);
                    let pageLink_ = pageUl.querySelectorAll("a");
                    let lastPage_ =  pageLink_.length - 2;
                    pageLi_ = pageUl.querySelectorAll('.list'); pageLi[0].classList.add("active");
                    pageRunner(pageLink_, itemPerPage, lastPage_, pageLi_);
                    
					pageMaker(index, items, active);
				}
			}

		}
		var pageLi = pageUl.querySelectorAll('.list'); pageLi[0].classList.add("active");
		pageRunner(pageLink, itemPerPage, lastPage, pageLi);

		function getpagElement(val){
			let pagelink = pageUl.querySelectorAll("a");
			let lastpage =  pagelink.length - 2;
			let pageli = pageUl.querySelectorAll('.list');
			pageli[0].classList.add("active");
			pageRunner(pagelink, val, lastpage, pageli);
			
		}
	
		
		
		function pageMaker(index, item_per_page, activePage){
			var shops_list = document.getElementById('shops_list').value
			window.location.href = "https://127.0.0.1/get_page" + "?page_number=" + index + "&shops_list=" + shops_list;
            const start = item_per_page * index;
			const end  = start + item_per_page;
			const current_page =  emptyBox.slice((start - item_per_page), (end-item_per_page));
			tbody.innerHTML = "";
			for(let j=0; j<current_page.length; j++){
				let item = current_page[j];					
				tbody.appendChild(item);
			}

		}





		// search content 
		var search = document.getElementById("search");
		search.onkeyup = e=>{
			const text = e.target.value;
			for(let i=0; i<tr.length; i++){
				const matchText = tr[i].querySelectorAll("td")[0].innerText;
				if(matchText.toLowerCase().indexOf(text.toLowerCase()) > -1){
					tr[i].style.visibility = "visible";
				}else{
					tr[i].style.visibility= "collapse";
				}
			}
		}
</script>
</body>
</html>
        """
	
    def get_text_tr(value):
        return f'<td>{value}</td>\n'
    def get_img_tr(value):
        return f'<td><img src={value}></td>\n'
    for product in products:
        if "amount" not in list(product.keys()):
            continue
        if "пакетик" in product['name']:
            continue
        if 'кг' in product['name']:
            product['amount'] = product['amount'] * 1000
        if 'мл' in product['name']:
            product['amount'] = product['amount'] / 1000
        
        start += "<tr>\n"
        start += get_text_tr(product["name"])
        start += get_img_tr(product["imageUrl"])
        if "priceBefore" in list(product.keys()):
            start += get_text_tr(product["priceBefore"])
        else:
            start += get_text_tr(product["priceAfter"])
        start += get_text_tr(product["priceAfter"])
        if "amount" in list(product.keys()):
            start += get_text_tr(product["amount"])
        else:
            start += get_text_tr(' ')
        
        if "discount" in list(product.keys()):
            start += get_text_tr(product["discount"])
        else:
            start += get_text_tr(str(0))
        
        start += get_text_tr(product["startDate"])
        start += get_text_tr(product["endDate"])
        start += "</tr>\n"
    start += end_table
    if ration_lines is not None:
        for elem in ration_lines:
            start += elem.replace('\n', '<br>')
    start += end_beg
    start += f'{end_middle} {page_number};\n'
    start += end_end_beg
    start += end_end_middle
    start += end_end_end
    return start

a = {
    'offer': [
        {
            'name': 'Вино Перохиль Бел. Сух. 0.75л', 
            'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/ht4mboaj2wq33un6g4j3n3u5wm.jpg', 
            'priceAfter': 299.99, 
            'amount': 0.75, 
            'startDate': '2023-03-30T00:00:00Z', 
            'endDate': '2023-04-30T00:00:00Z'
        }, 
        {
            'name': 'Вино Перохиль Крас. Сух. 0.75л', 
            'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/rmqkvp53ob424b3pp4kydcmsby.jpg', 
            'priceAfter': 299.99, 
            'amount': 0.75, 
            'startDate': '2023-03-30T00:00:00Z', 
            'endDate': '2023-04-30T00:00:00Z'
        }, 
        
        {'name': "Игристое вино Гиандая ламбруско эмилия бьянко амабиле'21 белое, полусладкое 0.75л", 
         'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/pfd5ovlhen3bf3gotgtaqwc5ca.jpg', 
         'priceBefore': 399.99, 
         'priceAfter': 279.99, 
         'amount': 0.75, 
         'discount': 31.0, 
         'startDate': '2023-03-29T00:00:00Z', 
         'endDate': '2023-04-25T00:00:00Z'
         }, {
    'name': "Вино Шардоне.новелла Тэйст'21 Белое, Сухое 0.75л",
      'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/pdjbjchiawr5fmhwo5zqmyswwa.jpg', 
      'priceBefore': 359.99, 
      'priceAfter': 259.99, 
 'amount': 0.75,
 'discount': 28.0,
 'startDate': '2023-03-29T00:00:00Z', 
 'endDate': '2023-04-25T00:00:00Z'}, {'name': "Вино Ликерное Крепленое Кагор Гурзуф'22 Красное, Десертное 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/joq3dey2hdhmdyospuo26k2ig4.jpg', 
 'priceAfter': 599.99, 
 'amount': 0.75, 
 'startDate': '2023-03-29T00:00:00Z', 
 'endDate': '2023-04-25T00:00:00Z'}, {'name': "Вино Меандер Шенен Блан'20/21 Бел.п/сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/zohyfglzj5ftjmmrflosdorbl4.jpg', 
 'priceAfter': 499.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Меандер Совиньон Блан'20/21 Бел.п/сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/fwt4od6ya5vsd2uerjf6s6gfoy.jpg', 
 'priceAfter': 499.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Оромо Шенен Блан'21 Бел.сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/o7jtrvrxbphkdrbssvjz3lsz4u.jpg', 
 'priceAfter': 449.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': 'Вино Кагор Десертное 0.75л', 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/35cvb5rc5qky2nytdp2rib7e6u.jpg', 
 'priceAfter': 499.99, 
 'amount': 0.75, 
 'startDate': '2023-03-29T00:00:00Z', 
 'endDate': '2023-04-25T00:00:00Z'}, {'name': "Вино Меандер Пинотаж'18/19/20 Крас.сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/psxkuz5tfzbupbbheypxqteloi.jpg', 
 'priceAfter': 499.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Вилла Лорен Бардолино'21 Крас.п/сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/opkbv36i2php7lckuav5onsqoa.jpg', 
 'priceAfter': 499.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Меандер Шираз'19/20 Крас.п/сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/4zz3vefwjyddirps6mo77k2z2q.jpg', 
 'priceAfter': 499.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Вилла Лорен Мерло'21 Крас.п/сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/rnkpzqfo5pvhdigwusubxtpqha.jpg', 
 'priceAfter': 499.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Шато О-лолион'19/20 Роз.сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/upvkmufprh4g6d7crslhxs5lcq.jpg', 
 'priceAfter': 699.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Винья Гормас Темпранильо'20/21 Красное, Сухое 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/uszz5irme7mp2rcozoea2xa2fy.jpg', 
 'priceBefore': 599.99, 
 'priceAfter': 499.99, 
 'amount': 0.75, 
 'discount': 17.0, 
 'startDate': '2023-03-29T00:00:00Z', 
 'endDate': '2023-04-25T00:00:00Z'}, {'name': "Вино Соаве Прима Альта'20/21 Белое, Сухое 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/i6vbuqi2qnwdf6awmmhebho4p4.jpg', 
 'priceBefore': 469.99, 
 'priceAfter': 369.99, 
 'amount': 0.75, 
 'discount': 22.0, 
 'startDate': '2023-03-29T00:00:00Z', 
 'endDate': '2023-04-25T00:00:00Z'}, {'name': "Вино Шато О-лолион'19/20 Бел.сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/ojjgrtosw2yzuhtidt5lzxc3ea.jpg', 
 'priceAfter': 599.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Алазанская Долина'20/21 Бел.п/слад. 0.75л /шуми", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/rhsmdiwlzoqunn7fatxdksaofi.jpg', 
 'priceAfter': 599.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Оромо Пинотаж'21 Крас.сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/slrufdudwcm5zesmhgrhnfxley.jpg', 
 'priceAfter': 449.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Дзингари Розато'20/21 Розовое, Сухое 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/bzumhpd5yroyxufsojydu6oug4.jpg', 
 'priceBefore': 1299.99, 
 'priceAfter': 999.99, 
 'amount': 0.75, 
 'discount': 24.0, 
 'startDate': '2023-03-29T00:00:00Z', 
 'endDate': '2023-04-25T00:00:00Z'}, {'name': "Вино Пино Гриджо Прима Альта'20/21 Белое, Сухое 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/bwoknxlpgoz6j6xfsh6roomdn4.jpg', 
 'priceBefore': 489.99, 
 'priceAfter': 389.99, 
 'amount': 0.75, 
 'discount': 21.0, 
 'startDate': '2023-03-29T00:00:00Z', 
 'endDate': '2023-04-25T00:00:00Z'}, {'name': "Вино Мерло Пулия'20/21 Терре Сакре Крас.сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/x26icf7wja5lslow43rggm3uym.jpg', 
 'priceAfter': 459.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Игристое вино кава ла Эспарденья'21 выдержанное розовое брют 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/xnajnvqhoadyoq6fjpvyy5pb7u.jpg', 
 'priceBefore': 599.99, 
 'priceAfter': 499.99, 
 'amount': 0.75, 
 'discount': 17.0, 
 'startDate': '2023-03-28T00:00:00Z', 
 'endDate': '2023-04-10T00:00:00Z'}, {'name': "Вино Плено Крианса'18 Выдерж.крас.сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/fimixven5giomdoxnqpaac6znu.jpg', 
 'priceAfter': 599.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Винья Масетеро Монастрель Апасионадо'20 Крас.п/сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/zpbldednbsehbpleszxocsz6ha.jpg', 
 'priceAfter': 599.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Мальвазия Бьянка Пулия'20/21 Терре Сакре Бел.п/сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/dv722ry2bdskaruz5afhltymne.jpg', 
 'priceAfter': 459.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Лос Сантос Айрен'20/21 Бел.п/слад. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/h6mjq75akd4tybgoholdin3itq.jpg', 
 'priceAfter': 399.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Лос Сантос Айрен'20/21 Бел.сух. 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/je3gv4bq7stt5njv6wnh3ekdoe.jpg', 
 'priceAfter': 399.99, 
 'amount': 0.75, 
 'startDate': '2023-03-30T00:00:00Z', 
 'endDate': '2023-04-30T00:00:00Z'}, {'name': "Вино Барон Симон'21 Белое, Полусладкое 0.75л", 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/vhbbjr4kwbikktpyuzsrtpo4ou.jpg', 
 'priceBefore': 359.99, 
 'priceAfter': 299.99, 
 'amount': 0.75, 
 'discount': 17.0, 
 'startDate': '2023-03-29T00:00:00Z', 
 'endDate': '2023-04-25T00:00:00Z'}, {'name': 'Коньяк ЖЮЛЬ ГОТРЕ 10 ЛЕТ 0.7л ПОДАРОЧНАЯ УПАКОВКА', 
 'imageUrl': 'https://leonardo.edadeal.io/dyn/cr/catalyst/offers/lsq4irccqlnmos5zt5qpfysvve.jpg', 
 'priceBefore': 4999.99, 
 'priceAfter': 3599.99, 
 'amount': 0.7, 
 'discount': 29.0, 
 'startDate': '2023-03-29T00:00:00Z', 
 'endDate': '2023-04-25T00:00:00Z'}]}


# with open('exmaple.json', 'wb') as fd:
#     fd.write(str(a).encode('utf-8'))

# html = handle_shop_resp(a['offer'])
# open('test.html', 'wb').write(html.encode('UTF-8'))    
