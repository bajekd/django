var context = document.getElementById('myChart').getContext('2d');
const getRandomType = () => {
  const types = [
    'bar',
    'horizontalBar',
    'pie',
    'line',
    'radar',
    'doughnut',
    'polarArea',
  ];
  return types[Math.floor(Math.random() * types.length)];
};

const displayChart = (data, labels) => {
  const type = getRandomType();
  var myChart = new Chart(context, {
    type: type, // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data: {
      labels: labels,
      datasets: [
        {
          label: `Amount (Last 6 months) (${type} View)`,
          data: data,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 99, 132,0.7)',
            'rgba(75, 192, 192, 0.2)',
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 99, 132,0.7)',
            'rgba(75, 192, 192, 1)',
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: 'Expense  Distribution Per Category',
        fontSize: 25,
      },
      legend: {
        display: true,
        position: 'right',
        labels: {
          fontColor: '#000',
        },
      },
    },
  });
};

const getChartData = () => {
  fetch('/expense_category_summary/')
    .then((res) => res.json())
    .then((results) => {
      const category_data = results.expenses_categories_data;
      const [labels, data] = [Object.keys(category_data), Object.values(category_data)]
      displayChart(data, labels);
    });
};

document.onload = getChartData();
