const app=require('./routes/index.js');

(async () => {
	app.listen(8080, '0.0.0.0', () => console.log('Listening on port 8080'));
})();
