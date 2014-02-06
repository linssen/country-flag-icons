<!doctype HTML>
<html>
	<head>
		<title>Flags preview</title>
		<style type="text/css">
			ul {margin: 0; padding: 0; list-style: none; width: 722px; margin: 0 auto; display: block; }
			li {float: left; margin-right: 5px; }

		</style>
	</head>
	<body>
	<ul>
		<% _.forEach(countries, function (country) { %>
			<li><img src="images/svg/<%- country.alpha3.toLowerCase() %>.svg" alt="<%- country.name %>" width="40" height="26"></li>
		<% }); %>
	</ul>
</body>
</html>