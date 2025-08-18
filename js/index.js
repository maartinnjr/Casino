document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('.header');
    let lastScrollY = window.scrollY;
    let scrollThreshold = 50;

    window.addEventListener('scroll', () => {
        if (window.scrollY > lastScrollY && window.scrollY > scrollThreshold) {
            header.classList.add('scrolled');
            header.classList.remove('up');
        } else if (window.scrollY < lastScrollY && window.scrollY > scrollThreshold) {
            header.classList.add('up');
        } else if (window.scrollY <= scrollThreshold) {
            header.classList.remove('scrolled');
            header.classList.remove('up');
        }
        lastScrollY = window.scrollY;
    });

    const hamburger = document.querySelector('.hamburger');
    const mainNav = document.querySelector('.main-nav');
    
    hamburger.addEventListener('click', function() {
        mainNav.classList.toggle('active');
    });

    // Cargar Puntuaciones
    function displayRanking(data) {
        const rankingBody = document.getElementById('ranking-body');
        if (!rankingBody) return;

        rankingBody.innerHTML = '';

        data.forEach((partida, index) => {
            const row = document.createElement('tr');
            
            // Contenido de la fila actualizado para el ranking
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${partida.usuario}</td> 
                <td>${partida.apuesta}</td>
                <td>${partida.tipo_moneda}</td>
            `;
            
            rankingBody.appendChild(row);
        });
    }

    // Obtener datos de la API
    async function fetchRanking() {
        try {
            const response = await fetch('http://localhost/api.php');
            const data = await response.json();
            
            displayRanking(data);

        } catch (error) {
            console.error('Error al obtener los datos del ranking:', error);
            const rankingBody = document.getElementById('ranking-body');
            if (rankingBody) {
                rankingBody.innerHTML = '<tr><td colspan="4">No se pudo cargar el ranking.</td></tr>';
            }
        }
    }

    fetchRanking();
});