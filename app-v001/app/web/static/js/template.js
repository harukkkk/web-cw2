$(function(){
    load();
    let titleInput = $('#title');
    titleInput.on("keydown", function(e){
        if(e.keyCode === 13){
            if(titleInput.val().length < 3 || titleInput.val().length > 128){
                alert("Write Something, accept 3 - 128 chars!");
            }else{
                // var local = getData();
                // local.push({
                //    title:$(this).val(),
                //    done: false
                // });
                // saveData(local);
                // load();
                // $(this).val("");
                createTodo();
            }
        }
    })

    $("ol,ul").on("click", "a", function(){
        // var data = getData();
        let a = $(this);
        let index = a.attr("id");
        let st = a.attr("data-status")
        if (st === 'true'){
            markUndone(index)
        } else{
            markDone(index)
        }
        // data.splice(index,1);
        // saveData(data);
        // load();

    })

    $("ol,ul").on("click","input", function(){
        // var data = getData();
        let a = $(this).siblings("a");
        let index = a.attr("id");
        let st = a.attr("data-status")
        if (st === 'true'){
            markUndone(index)
        } else{
            markDone(index)
        }
        // data[index].done = $(this).prop("checked");
        // saveData(data);
        // load();
    })

    function getData(){
        var data = localStorage.getItem("todo-list");
        if(data!=null){
            return JSON.parse(data);
        }else{
            return [];
        }
    }

    function saveData(data){
        localStorage.setItem("todo-list",JSON.stringify(data))
    }

    function load() {
        $( "ol,ul" ).empty();

        $.ajax( {
            url: '/todo/list',
            type: 'get',
            success: function ( res ) {
                let todoCount = 0;
                let doneCount = 0;

                $.each( res.data, function ( indexInArray, valueOfElement ) {
                    if ( valueOfElement.done === true ) {
                        $( "ul" ).prepend( `<li><input type="checkbox" checked="checked"><p>${valueOfElement.title} - ${valueOfElement.created_at}</p><a href="javascript:;" id=${valueOfElement.id} data-status="${valueOfElement.done}"></a></li>`);
                        doneCount++;
                    }
                    else {
                        $( "ol" ).prepend( `<li><input type="checkbox"><p>${valueOfElement.title} - ${valueOfElement.created_at}</p><a href="javascript:;" id=${valueOfElement.id} data-status="${valueOfElement.done}"></a></li>` );
                        todoCount++;
                    }

                    if ( $( 'ul>li' ).length == 0 ) {
                        $( '#done-count' ).hide( 300 );
                    }
                    else {
                        $( '#done-count' ).show( 300 );
                    }
                    if ( $( 'ol>li' ).length == 0 ) {
                        $( '#todo-count' ).hide( 300 );
                    }
                    else {
                        $( '#todo-count' ).show( 300 );
                    }
                } );
                $( "#todo-count" ).text( todoCount );
                $( "#done-count" ).text( doneCount );
            }
        } )
    }
    console.log($('ul>li').length);

    function createTodo() {
        let content = window.btoa(titleInput.val())
        $.ajax({
            url: '/todo/create/' + content,
            type: 'get',
            success: function ( res ){
                console.log(res)
                if (res.status === 'success'){
                    titleInput.val();
                    load();
                }
            }
        })
    }
    function markDone(tid){
        $.ajax({
            url: `/todo/mark_done/${tid}`,
            type: 'get',
            success: function ( res ){
                load()
            }
        })
    }
    function markUndone(tid){
        $.ajax({
            url: `/todo/mark_undone/${tid}`,
            type: 'get',
            success: function ( res ){
                load()
            }
        })
    }

})