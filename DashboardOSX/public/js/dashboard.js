$(document).ready(function() {

	Array.prototype.contains = function ( needle ) {
	for (i in this) {
    	if (this[i] === needle) return true;
	}
	return false;
	}


	$.get('/getUnity', function(response) {
		$('header h2').append(response);
	});
	
	updateState();
	setInterval(updateState,5000);
	$.getJSON('/CSC591_advancedalgos_tasks.json',function(data) {
		$('#tagNameInput').typeahead({source:data});
	});

	$('#myModal').on('show.bs.modal', function (event) {
    	$('#tagNameInput').focus();
    	var file = $(event.relatedTarget).data('file');
    	var type = $(event.relatedTarget).data('type');
    	$('#myModal').attr('data-file',file);
    	$('#myModal').attr('data-type',type);
    	
  	});

  	$('#myModalClose').click(function(){
  		$('#myModal').modal('hide');
  		var tag = $('#tagNameInput').val();
  		if (tag !== null && tag!== '') {
  			
  			var file =$('#myModal').attr('data-file');
  			var type=$('#myModal').attr('data-type');
  			
  			if (type==='file') {
				file = file.replace(/\//g,":");
				var url='/addTag/';
				
				$.get(url+tag+'/'+file, function(response) {
					updateState();
				});
			}
			else{
				//file=encodeURIComponent(file);
				var url = '/addTagURL';

				data={'url':file,'tag':tag};
				$.post(url,data,function(response) {
					updateState();
				});

			}
  			
  		}

  	});

});

function updateState() {


	$.getJSON('/getState',function(data) {
	//data=JSON.parse(data);
		$('.content').html("");
		var tasks = Object.keys(data);
		$.each(tasks, function(index,task){
			var html='';
			var files = Object.keys(data[task])
			$.each(files,function(index,file){
				html+=getFileEntryHTML(file,data[task][file].EvtTime,task,data[task][file].type)
			});
			var html='<ul class="list-group">'+html+'</ul>';

			var tagHeader = '<div class="row"> \
				<div class="col-md-12">      \
				<h3>' + task + '&nbsp;<button data-tag='+task+' class=" btn btn-sm btn-primary action-clear-tag"> \
					<span class="glyphicon glyphicon-trash"></span></button>	\
					<button class="btn btn-sm btn-primary action-open-all" data-tag=' + task + '>Open All</button>	\
				</h3></div> \
			  </div>';
			$('.content').append(tagHeader);
			$('.content').append(html);
		});

		//Highlight the first task
		//$('.content ul:first').css('background-color','red');
		setClickHandlers();
	});
}


function getFileEntryHTML(file,time,task,type)
{
	time=moment(time/1000,'X').fromNow();
	//return '<li class="list-group-item">'+time+"  <span>"+file+'</span></li>';

	if(type=='file') {
		
		
		return '<li class="list-group-item" data-task='+ task +'><div class="row">  \
			<div class="col-md-2">' + time +'</div>     \
			<div class="col-md-6">' + file +'</div>     \
			<div class="col-md-4">' + "" +'     \
			<div class="btn-group">  \
	  			<button type="button" class="btn btn-sm btn-primary action-open"  data-file="'+file+'">Open</button>   \
	  			<button type="button" class="btn btn-sm btn-primary dropdown-toggle" data-toggle="dropdown" aria-expanded="false">   \
	  			    <span class="caret"></span>  \
	    			<span class="sr-only">Toggle Dropdown</span>  \
	  			</button>  \
	  			<ul class="dropdown-menu" role="menu">  \
	    			<li><a href="#" class="action-show" data-file="'+file+'">Open in File Browser</a></li>  \
	    		</ul>  \
			</div>   \
			<!--<button class="btn btn-sm btn-primary action-tag" data-toggle="modal" data-target="#myModal" data-type="'+type+'" data-file="'+file+'"">Tag</button>--> \
			<div class="btn-group">  \
  				<button type="button" class="btn btn-sm btn-primary action-showtag"  data-file="'+file+'">Tag</button>   \
  				<button type="button" class="btn btn-sm btn-primary dropdown-toggle" data-toggle="dropdown" aria-expanded="false">   \
  			    	<span class="caret"></span>  \
    				<span class="sr-only">Toggle Dropdown</span>  \
  				</button>  \
  				<ul class="dropdown-menu" role="menu">  \
    				<li><a href="#" class="action-addtag" data-toggle="modal" data-target="#myModal" data-type="'+type+'" data-file="'+file+'">Add Tag</a></li>  \
    				<li><a href="#" class="action-removetag" data-type="'+type+'" data-file="'+file+'"  data-task='+ task +'>Remove Tag</a></li>  \
    			</ul>  \
			</div>   \
			<button class="btn btn-sm btn-primary action-showsum" '+ fileSummaryDisabledState(file)+' data-type="'+type+'" data-file="'+file+'"">Summary</button> \
			<button class="btn btn-sm btn-primary action-uploadfile" '+ fileSummaryDisabledState(file)+'  data-task="'+ task +'""  data-type="'+type+'" data-file="'+file+'"">Upload</button> \
			</div>   \
		</div></li>';

	}
	else if (type=='url') {
		link = '<a target="_blank" href="'+file+'"">'+file+'</a>'

		return '<li class="list-group-item" data-task='+ task +'><div class="row">  \
			<div class="col-md-2">' + time +'</div>     \
			<div class="col-md-6">' + link +'</div>     \
			<div class="col-md-4">' + "" +'     \
				<a role="button" target="_blank" href="'+file+'" class="btn btn-sm btn-primary ">Open</a> \
				<div class="btn-group">  \
	  				<button type="button" class="btn btn-sm btn-primary action-showtag"  data-file="'+file+'">Tag</button>   \
	  				<button type="button" class="btn btn-sm btn-primary dropdown-toggle" data-toggle="dropdown" aria-expanded="false">   \
	  			    	<span class="caret"></span>  \
	    				<span class="sr-only">Toggle Dropdown</span>  \
	  				</button>  \
	  				<ul class="dropdown-menu" role="menu">  \
	    				<li><a href="#" class="action-addtag" data-toggle="modal" data-target="#myModal" data-type="'+type+'" data-file="'+file+'">Add Tag</a></li>  \
	    				<li><a href="#" class="action-removetag" data-type="'+type+'" data-file="'+file+'"  data-task="'+ task +'"">Remove Tag</a></li>  \
	    			</ul>  \
				</div>   \
			</div>   \
		</div></li>';


	}

}


function setClickHandlers() {
	$('li button.action-open ').click(function(event) {
		//var file = $(this).parent().parent().parent().children('.col-md-7').html();
		//alert(file);
		var file = $(this).data('file');
		file = file.replace(/\//g,":")
		$.get('/openFile/'+(file), function(response){
			console.log(response);
		});
	});

	$('li a.action-show').click(function(event) {
		//var file = $(this).parent().parent().parent().parent().parent().children('.col-md-7').html();
		//alert(file);
		var file = $(this).data('file');
		file = file.replace(/\//g,":")
		$.get('/openInBrowser/'+(file), function(response){
			console.log(response);
		});
	});

	$('li button.action-tag ').each(function() {
		var tag = $(this).parent().parent().parent().attr('data-task');
		if (tag=='Untagged') {
			$(this).html("Add tag");
			//setAddTagClickHandler($(this));
		}
		else {
			$(this).html("Remove tag");
			setRemoveTagClickHandler($(this),tag);
		}
	});

	$('.action-removetag').each(function () {
		var file = $(this).data('file');
		var task = $(this).data('task');
		setRemoveTagClickHandler($(this),task)
	});


	$('.action-clear-tag').click(function(event) {
		var tag = $(this).data('tag');
		$.getJSON('/clearTag/'+tag, function(response) {
			updateState();
		});

	});

	$('.action-open-all').click(function(event) {
		var tag = $(this).data('tag');
		$.getJSON('/openAll/'+tag, function(response) {
			$.each(response.listOfURLs,function(i,item) {
				$("#dummyLink").attr("href", item).attr("target", "_blank")[0].click();
			});
		});
	});

	$('.action-showtag').click(function() {
		var file = $(this).data('file');
		//file = file.replace(/\//g,":");
		data={'filepath':file};
		//file = encodeURIComponent(file);
		$.post('/getAllTagsByFile',data,function(response) {
			//response=JSON.parse(response);
			$('#alertModalContent').html(formatTagList(response.result));
			$('#alertModal').modal('show');
		});
	});

	$('.action-showsum').click(function() {
		var file = $(this).data('file');
		data={'filepath':file};
		$.post('/getSummary',data,function(response) {
			$('#alertModalContent').html(response.summary.join("	"));
			$('#alertModal').modal('show');
		});
	});


	$('.action-uploadfile').click(function() {
		var file = $(this).data('file');
		var task = $(this).data('task');
		data={'filepath':file, 'task': task};
		$.post('/uploadDocument',data,function(response) {
			$('#alertModalContent').html("File upload Successfull");
			$('#alertModal').modal('show');
		});
	})

}

function setAddTagClickHandler(button) {

	button.click(function() {
		var file = $(this).parent().parent().children('.col-md-7').html();
		file = file.replace(/\//g,":");
		tag = prompt("Enter Tag for the file");
		$.get('/addTag/'+tag+'/'+file, function(response) {
			updateState();
		});
	});

}

function setRemoveTagClickHandler(button,tag) {

	//button.attr("data-target","");
	//button.attr("data-toggle","");
	button.click(function(event) {
		//var file = $(this).parent().parent().children('.col-md-7').html();
		var file = button.data('file');
		var type=button.data('type');
		//alert(file);
		if (type==='file') {
			file = file.replace(/\//g,":");
			var url='/removeTag/';

			$.getJSON(url+tag+'/'+file,function(response) {
				updateState();
			});
		}
		else
		{
			//file = file.replace(/\//g,"|");
			var url = '/removeTagURL';
			var data = {'url':file,'tag':tag};
			//data.url=url;
			//data.tag=tag;
			$.post(url,data, function(response) {
				updateState();
			});
		}
	});

}

function formatTagList(list) {
	if (list.length==0) {
		return "This file/url is not tagged";
	}
	else 
	{
		out="";
		for (var i = list.length - 1; i >= 0; i--) 
		{
			out+=(list[i]+'<br/>');		
		}
		return out;
	}
}

function fileSummaryDisabledState(file) {
	var supportedFormats=["doc","docx","pdf","ppt","pptx","txt"];

	var arr = file.split(".");
	var ext = arr[arr.length-1];

	if (supportedFormats.contains(ext)) {
		return "";
	}
	else {
		return "disabled";
	}

}