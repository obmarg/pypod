<html>
	<head>
		<title>
		Pypod
		</title>
	<script type='text/javascript' src='jquery.js' ></script>
    <script type='text/javascript' src='jquery-ui.js' ></script>
    <link rel='stylesheet' type='text/css' href='jquery-ui.css' />
    </head>
    <style type='text/css'>
        html {
			text-align: center;
        }

		#controlPanel {
			padding: 6px;
			display: inline-block;
		}

		#podcastListContainer {
			display:inline-block; 
		}

		#podcastList {
			list-style-type: none;
			margin: 0;
			padding: 0;
		}

		#podcastList li {
			margin: 3px;
			padding: 0.4em;
			font-size: 1.4em;
			height: 18px;
			display: inline-block;
		}

		.deletePodcast {
			display: inline-block;
		}

		#addPodcastForm {
			text-align: left;
			font-size: 62.5%;
		}

		#confirmDeleteDialog {
			vertical-align: middle;
			text-align: center;
		}

		#podcastDownloadRadio {
			text-align: center;
		}

		label, input { display:block; }
		input.text { margin-bottom:12px; width:95%; padding: .4em; }
		fieldset { padding:0; border:0; margin-top:25px; }
		.ui-dialog .ui-state-error { padding: .3em; }
		.validateTips { border: 1px solid transparent; padding: 0.3em; }
    </style>
	<script type='text/javascript'>
        var currentDelete = "";
		$(function(){
			$( "#addPodcast" ).button({
				text : false,
				icons : {
					primary: "ui-icon-plus"
				}
			});
			$( "#refresh" ).button({
				text : false,
				icons : {
					primary: "ui-icon-refresh"
				}
			});
			$( ".deletePodcast" ).button({
				text : false,
				icons : {
					primary: "ui-icon-delete"
				}
			});

			var addPodcastFields = $( [] )
				.add( "#name" )
				.add( "#feedUrl" )
				.add( "#downloadOnlyNewPodcasts" )
				.add( "#downloadAllPodcasts" )
	
			$( "#addPodcastForm" ).dialog({
				autoOpen : false,
				height : 400,
				width : 450,
				modal : true,
				show : 'slide',
				hide : 'slide',
				buttons : {
					"Add Podcast" : function(){
						//TODO: Verify shit
						var name = $( "#name" ).val();
                        var url = $( "#feedUrl" ).val();
                        var downloadAll = $( "input[name=downloadAllRadio]:checked" ).index()
						$.post( 
							'api/addPodcast',
							{ 'name' : name, 'url' : url, 'da' : downloadAll },
							function( data ){
								//TODO: Do something with the returned data
								// For now though, just reload the page
								location.reload();
							}
						);
                        $( this ).dialog( "close" );
					},
					"Cancel" : function(){
						$( this ).dialog( "close" );
					}
				},
				close : function(){
					addPodcastFields.val( "" ).removeClass( "ui-state-error" );
				}
			});

			$( "#confirmDeleteDialog" ).dialog({
				autoOpen : false,
				resizable : false,
				modal : true,
				buttons : {
					"Yes" : function(){
                        $.post(
                            'api/removePodcast',
                            { 'name' : currentDelete },
                            function( data ){
                                //Do something and refresh.
                                // For now, just refresh
                                location.reload();
                            }
                        );
                        $( this ).dialog( "close" );
					},
					"No" : function(){
                        currentDelete = ""
						$( this ).dialog( "close" );
					}
				}
			});

			$( "#podcastDownloadRadio" ).buttonset();

			$( "#addPodcast" ).click( function() {
				$( "#addPodcastForm" ).dialog( "open" );
			});

			$( ".deletePodcast" ).click( function(){
                currentDelete = $( this ).attr( "name" );
				$( "#confirmDeleteDialog" ).dialog( "open" );
			});
		});
	</script>
	<body>
        <div id="controlPanel" class='ui-widget-header ui-corner-all'>
			<button id="addPodcast" > Add Podcast </button>
			<button id="refresh" > Refresh </button>
        </div>
		<div />
        <div id="podcastListContainer" ><ul id="podcastList">
	        {% for p in podcasts %}
                <div class='ui-widget-content'>
                    <li> {{ p.name }} </li><button class="deletePodcast" name="{{ p.name }}" > Delete </button>
                </div>
            {% endfor %}
        </ul></div>
		<div id="addPodcastForm" title="Add Podcast">
			<p class='validateTips'>All fields are required</p>

			<form>
			<fieldset>
				<label for="name">Name</label>
				<input type='text' name='name' id='name' class='text ui-widget-content ui-corner-all' />
				<label for="feedUrl">Feed URL</label>
				<input type='text' name='feedUrl' id='feedUrl' class='text ui-widget-content ui-corner-all' />
				<div id="podcastDownloadRadio">
					<input type='radio' id="downloadOnlyNewPodcasts" name="downloadAllRadio" /><label for="downloadOnlyNewPodcasts">Download Only New Podcasts</label></input>
					<input type='radio' id="downloadAllPodcasts" name="downloadAllRadio" /><label for="downloadAllPodcasts">Download All Avaliable Podcasts</label></input>
				</div>
			</fieldset>
			</form>
		</div>
		<div id="confirmDeleteDialog" title="Confirm Delete?">
			Are you sure you want to delete this podcast?
		</div>
	</body>
</html>
