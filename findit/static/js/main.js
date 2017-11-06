$(document).ready(function() {
	$('[data-toggle="tooltip"]').tooltip();
	new Chart(document.getElementById("line-chart"), {
		  type: 'line',
		  data: {
		    labels: ['Mon','tues'],
		    datasets: [{ 
		        data: [1,5,9],
		        label: "Clicks",
		        borderColor: "#3e95cd",
		        backgroundColor: '#3e95cd',
		        fill: false
		      }, { 
		        data: [9,2,3],
		        label: "Views",
		        borderColor: "#e807f5",
		        backgroundColor: '#e201f5',
		        fill: false
		      }
		    ]
		  },
		  options: {
		    title: {
		      display: true,
		      text: 'Ad performance'
		    }
		  }
		});
})