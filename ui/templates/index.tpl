<html>
    <head>
        <title>
        Pypod
        </title>
    <script type='text/javascript' src='jquery.js' ></script>
    <script type='text/javascript' src='jquery-ui.js' ></script>
    <script type='text/javascript' src='jquery.qtip.js' ></script>
    <link rel='stylesheet' type='text/css' href='jquery-ui.css' />
    <link rel='stylesheet' type='text/css' href='jquery.qtip.css' />
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
            vertical-align: middle;
        }

        #podcastList button {
            display: inline-block;
            margin: 3px;
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
        function updateTips( tips, text, tabIndex ) {
            if( tabIndex != undefined ) {
                $( "#addPodcastFormTabs" ).tabs( "select", tabIndex );
            }
            tips
                .text( text )
                .addClass( 'ui-state-highlight' );
            setTimeout(function(){
                    tips.removeClass( 'ui-state-highlight', 1500 );
                }, 500 
            );
        }

        {% if podcastNames|length > 0 %}
        existingNames = [ '{{ podcastNames|join('\', \'') }}' ];
        {% else %}
        existingNames = []
        {% endif %}
        
        function resetValidateTips( fields, which ) {
            var updateBasic = true;
            var updateAdvanced = true;
            if ( which != undefined ) {
                if ( which == 0 ) {
                    updateAdvanced = false;
                } else {
                    updateBasic = false;
                }
            }
            if( updateBasic ) {
                $( "#addPodcastBasicTips" ).text( 
                    "All fields are required" 
                    );
            }
            if( updateAdvanced ) { 
                $( "#addPodcastAdvancedTips" ).text(
                    "Mouse over for help text"
                    );
            }
            if( fields ) {
                fields.removeClass( 'ui-state-error' );
            }
        }

        function validateName( name, resetTips ) {
            if( resetTips ) {
                resetValidateTips( name, 0 );
            }
            var errMsg = ""
            if( !name.val() ) {
                errMsg = "Name must not be empty";
            } else {
                var nameStr = name.val();
                for( var i = 0; i < existingNames.length; i++ ) {
                    if( nameStr == existingNames[ i ] ) {
                        errMsg = "There is already a podcast named " + nameStr;
                    }
                }
            }
            if( errMsg != "" ) {
                name.addClass( "ui-state-error" );
                updateTips(
                    $( "#addPodcastBasicTips" ),
                    errMsg,
                    0
                    );
                return false;
            }
            return true;
        }

        function validateUrl( url, resetTips ) {
            if( resetTips ) {
                resetValidateTips( url, 0 );
            }
            if( !url.val() || 
                ( 
                    ( url.val().search( "http://" ) != 0 ) && 
                    ( url.val().search( "https://") != 0 )
                ) )
            {
                url.addClass( "ui-state-error" );
                updateTips(
                    $( "#addPodcastBasicTips" ),
                    "Feed URL must begin with http:// or https://",
                    0
                    );
            }
            else if( url.val().length < 9 )
            {
                url.addClass( "ui-state-error" );
                updateTips(
                    $( "#addPodcastBasicTips" ),
                    "Feed URL must contain a url",
                    0
                    );
            }
            return true;
        }
        
        function validateDownloadAll( downloadAll ) {
            if( downloadAll != 0 && downloadAll != 2 )
            {
                updateTips( 
                    $( "#addPodcastBasicTips" ),
                    "You must select either download all or only new",
                    0
                    );
                return false;
            }
            return true;
        }

        function validateDestFilenameFormat( filenameFormat, resetTips ) {
            if( resetTips ) {
                resetValidateTips( filenameFormat, 1 );
            }
            if( !filenameFormat.val() ) {
                filenameFormat.addClass( 'ui-state-error' );
                updateTips(
                    $( "#addPodcastAdvancedTips" ),
                    "The podcast destination filename format can't be empty",
                    1
                    );
                return false;
            }
            else
            {
                var format = filenameFormat.val();
                var ok = true;
                if( format.search( "~" ) != -1 ) {
                    ok = false;
                }
                if( format.search( "^/" ) != -1 ) {
                    ok = false;
                }
                if( format.search( "\\.\\." ) != -1 ) {
                    ok = false;
                }
                if( !ok ) {
                    filenameFormat.addClass( "ui-state-error" );
                    updateTips( 
                        $( "#addPodcastAdvancedTips" ),
                        "The podcast destination format must be a relative path",
                        1
                        );
                    return false;
                }
            }
            return true;
        }

        function validatePodcastFields( fields ) {
            resetValidateTips( fields );
            var rv = 
                validateName( $("#name"), false ) &&
                validateUrl( $("#feedUrl"), false ) && 
                validateDownloadAll( 
                    $( "input[name=downloadAllRadio]:checked" ).index(),
                    false
                    ) &&
                validateDestFilenameFormat( $( "#destFilenameFormat" ), false );
            return rv;
        }

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
                .add( "#destFilenameFormat" );

            $( "#name" ).change(function(){
                validateName( $( this ), true );
            });

            $( "#feedUrl" ).change(function(){
                validateUrl( $( this ), true );
            });

            $( "#destFilenameFormat" ).change(function(){
                validateDestFilenameFormat( $( this ), true );
            });

            $( "#addPodcastForm" ).dialog({
                autoOpen : false,
                height : 400,
                width : 450,
                modal : true,
                show : 'slide',
                hide : 'slide',
                buttons : {
                    "Add Podcast" : function(){
                        var name = $( "#name" ).val();
                        var url = $( "#feedUrl" ).val();
                        var downloadAll = 
                            $( "input[name=downloadAllRadio]:checked" ).index();
                        var filenameFormat = $( "#destFilenameFormat" ).val();

                        if( !validatePodcastFields( addPodcastFields ) ) {
                                return;
                        }
                        $.post( 
                            'api/addPodcast',
                            { 
                                'name' : name, 
                                'url' : url, 
                                'da' : downloadAll,
                                'filenameFormat' : filenameFormat
                            },
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
                open : function(){
                    addPodcastFields.val( "" );
                    $( "#destFilenameFormat" ).val( 
                        "{{ defaultDestFilenameFormat  }}" 
                        );
                    $( "#addPodcastFormTabs" ).tabs( "select", 0 );
                    resetValidateTips( addPodcastFields );
                },
                close : function(){
                    addPodcastFields.val( "" );
                    resetValidateTips( addPodcastFields );
                }
            });

            $( "#addPodcastFormTabs" ).tabs();

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

            $( "input[title]" ).qtip({
                tip : true
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
            <div id="addPodcastFormTabs">
                <ul>
                    <li><a href='#addPodcastBasicSettings'>Basic Settings</a></li>
                    <li><a href='#addPodcastAdvancedSettings'>Advanced Settings</a></li>
                </ul>
                <div id='addPodcastBasicSettings'>
                    <p id='addPodcastBasicTips' class='validateTips'>SOMETHING:</p>

                    <form>
                    <fieldset>
                        <label for="name">Name</label>
                        <input 
                            type='text' 
                            name='name' 
                            id='name' 
                            class='text ui-widget-content ui-corner-all'
                            title='The name of the podcast.  This will also be used as the folder name'
                            />
                        <label for="feedUrl">Feed URL</label>
                        <input 
                            type='text' 
                            name='feedUrl' 
                            id='feedUrl' 
                            class='text ui-widget-content ui-corner-all'
                            title='The HTTP url to the RSS Feed'
                            />
                        <div id="podcastDownloadRadio">
                            <input 
                                type="radio" 
                                id="downloadOnlyNewPodcasts"
                                name="downloadAllRadio"
                                />
                                <label for="downloadOnlyNewPodcasts">
                                    Only Download New Podcasts
                                </label>
                            </input>
                            <input 
                                type='radio' 
                                id="downloadAllPodcasts" 
                                name="downloadAllRadio" 
                                />
                                <label for="downloadAllPodcasts">
                                    Download All Avaliable Podcasts
                                </label>
                            </input>
                        </div>
                    </fieldset>
                    </form>
                </div>
                <div id="addPodcastAdvancedSettings">
                    <p id="addPodcastAdvancedTips" class='validateTips' >SOMETHING:</p>

                    <form>
                    <fieldset>
                        <label for="destFilenameFormat" >Destination Filename Format</label>
                        <input 
                            type="text" 
                            id="destFilenameFormat" 
                            name="destFilenameFormat" 
                            class='text ui-widget-content ui-corner-all'
                            title='The format for destination files. <br /> {{ destFilenameFormatHelp }}'
                            />
                    </fieldset>
                    </form>
                </div>
            </div>
        </div>
        <div id="confirmDeleteDialog" title="Confirm Delete?">
            Are you sure you want to delete this podcast?
        </div>
    </body>
</html>
