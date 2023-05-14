$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})
//while clicking (+)
$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString(); // get the id from addtocart.html (pid="{{cart.product.id})ok
    var eml = this.parentNode.children[2] // the parentNode is <div class="my-3"> and children[2] means 0,1,2 i.e 3 position i.e (span tag) of addtocart.html ok 
    console.log(id);
    $.ajax({
        type:'GET',
        url:"/pluscart", //it hit the url so looked at url.py
        data:{
            prod_id:id //this is return to Plus_cart functn where it become(prod_id = request.GET['prod_id'])ok
        },
        success: function(data){  // here it get the data when JsonResponse(data) returned from Plus_cart functn ok
            console.log(data)
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})

//while clicking (-)
$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString(); // get the id from addtocart.html (pid="{{cart.product.id})ok
    var eml = this.parentNode.children[2] // the parentNode is <div class="my-3"> and children[2] means 0,1,2 i.e 3 position i.e (span tag) of addtocart.html ok 
    //console.log(id);
    $.ajax({
        type:'GET',
        url:"/minuscart", //it hit the url so looked at url.py
        data:{
            prod_id:id //this is return to Plus_cart functn where it become(prod_id = request.GET['prod_id'])ok
        },
        success: function(data){  // here it get the data when JsonResponse(data) returned from Plus_cart functn ok
            //console.log(data)
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString(); // get the id from addtocart.html (pid="{{cart.product.id})ok
    var eml = this 
    //console.log(id);
    $.ajax({
        type:'GET',
        url:"/removecart", //it hit the url so looked at url.py
        data:{
            prod_id:id //this is return to Plus_cart functn where it become(prod_id = request.GET['prod_id'])ok
        },
        success: function(data){  // here it get the data when JsonResponse(data) returned from Plus_cart functn ok
            //console.log(data)
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()// deleting the parent of parent div so that nomore remain in addtocart ,that whole div is deleted 
            //when line number 29 is clicked i.e Remove item then its parent is lin no 28 div ok and its parent is line no 19 and its parent is 18(class="col-sm-9") and again its parent div is line no 14(class="row")
            // that means 4 parentnode are there 
        }
    })
})
