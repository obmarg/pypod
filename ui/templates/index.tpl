<html>
	<head>
		<title>
		Working!!!!!!
		</title>
	<script type='text/javascript' src='jquery.js' ></script>
    <script type='text/javascript' src='jquery-ui.js' ></script>
    <link rel='stylesheet' type='text/css' href='jquery-ui.css' />
    </head>
    <style type='text/css'>
        html {
            background: 
        }
    </style>
	<body>
        <div id="controlPanel">
            <a href='link'>Add Podcast</a>
        </div>
        <div id="podcastList" ><ul>
	        {% for p in podcasts %}
                <li>{{ p.title }}</li>
            {% endfor %}
        </ul></div>
	</body>
</html>
