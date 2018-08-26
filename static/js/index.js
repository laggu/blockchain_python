generatekey = function(){
    keyword = $("keyword").innerText
    jsondata = JSON.stringify({keyword : keyword});
    $.ajax({
        type : "GET",
        url : "/generatekey",
        data : jsondata,
        dataType : "json",
        error : function(){
            alert('통신실패!!');
        },
        success : function(data){
            alert("통신데이터 값 : " + data);
            $("#myPriv").html(data.myPriv);
            $("#myPubl").html(data.myPubl);
            $("#myAddr").html(data.myAddress);
            $("#message").html("종이에 꼭 적어두세요!");
        }
    });
};

mining = function(){
    jsondata = JSON.stringify({minerAddress : $("#minerAddress").innerText});
    $.ajax({
        type : "GET",
        url : "/mining",
        data : jsondata,
        dataType : "json",
        error : function(){
            alert('통신실패!!');
        },
        success : function(data){
            alert("통신데이터 값 : " + data) ;
            $("#blockhash").html(data.blockhash) ;
        }
    });
};

transaction = function(){
    jsondata = JSON.stringify(
            {
                senderAddress : $("#senderAddress").innerText,
                receiverAddress : $("#receiverAddress").innerText,
                value : $("#value").innerText,
                senderPriv : $("#senderPriv").innerText,
            }
        );
    $.ajax({
        type : "GET",
        url : "/transaction",
        data : jsondata,
        dataType : "json",
        error : function(){
            alert('통신실패!!');
        },
        success : function(data){
            alert("통신데이터 값 : " + data) ;
            $("#txhash").html(data.txhash) ;
        }
    });
};

balance = function(){
    jsondata = JSON.stringify({balance : $("#balance").innerText});
    $.ajax({
        type : "GET",
        url : "/balance",
        data : jsondata,
        dataType : "json",
        error : function(){
            alert('통신실패!!');
        },
        success : function(data){
            alert("통신데이터 값 : " + data) ;
            $("#balance").html(balance) ;
        }
    });
};

checkBlock = function(){
    jsondata = JSON.stringify({blockHash : $("#checkblock_hash").innerText});
    $.ajax({
        type : "GET",
        url : "/checkBlock",
        data : jsondata,
        dataType : "json",
        error : function(){
            alert('통신실패!!');
        },
        success : function(data){
            $("#checkedBlock").html(data.block);
        }
    });
};

$(document).ready(function(){
    $('#generatekey_btn').onclick = generatekey;
    $('#mining_btn').onclick = mining;
    $('#transaction_btn').onclick = transaction;
    $('#balance_btn').onclick = balance;
    $('#checkBlock_btn').onclick = checkBlock;
});
