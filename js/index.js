document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('.header');
    const hamburger = document.querySelector('.hamburger');
    const mainNav = document.querySelector('.main-nav');
    let lastScrollY = window.scrollY;

    hamburger.addEventListener('click', function() {
        const isOpening = !mainNav.classList.contains('active');
        mainNav.classList.toggle('active');
        hamburger.classList.toggle('is-active');

        if (isOpening) {
            header.classList.remove('scrolled', 'up');
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    });

    window.addEventListener('scroll', () => {
        if (!mainNav.classList.contains('active')) {
            if (window.scrollY > lastScrollY && window.scrollY > 100) {
                header.classList.add('scrolled');
                header.classList.remove('up');
            } else if (window.scrollY < lastScrollY) {
                header.classList.add('up');
            }
            if (window.scrollY <= 50) {
                 header.classList.remove('scrolled', 'up');
            }
            lastScrollY = window.scrollY;
        }
    });

    // --- LÓGICA PARA EL HISTORIAL DE PARTIDAS ---
    function displayGameHistory(data) {
        const rankingBody = document.getElementById('ranking-body');
        if (!rankingBody) return;

        rankingBody.innerHTML = '';
        data.forEach((partida) => {
            const row = document.createElement('tr');
            let resultadoClase = '';
            let resultadoTexto = '';

            switch (partida.resultado) {
                case 'ganaste': resultadoClase = 'resultado-ganaste'; resultadoTexto = 'Ganó'; break;
                case 'perdiste': resultadoClase = 'resultado-perdiste'; resultadoTexto = 'Perdió'; break;
                case 'empate': resultadoClase = 'resultado-empate'; resultadoTexto = 'Empate'; break;
                default: resultadoTexto = partida.resultado;
            }

            const fecha = new Date(partida.fecha);
            const fechaFormateada = `${String(fecha.getDate()).padStart(2, '0')}/${String(fecha.getMonth() + 1).padStart(2, '0')} ${String(fecha.getHours()).padStart(2, '0')}:${String(fecha.getMinutes()).padStart(2, '0')}`;
            
            row.innerHTML = `<td data-label="Fecha">${fechaFormateada}</td><td data-label="Nombre">${partida.usuario}</td><td data-label="Apostó">${partida.apuesta}</td><td data-label="Juego">${partida.nombre_juego}</td><td data-label="Resultado"><span class="${resultadoClase}">${resultadoTexto}</span></td>`;
            rankingBody.appendChild(row);
        });
    }

    async function fetchGameHistory() {
        try {
            const response = await fetch('/Casino_Local/api/API.php?accion=historial');
            const data = await response.json();
            displayGameHistory(data);
        } catch (error) {
            console.error('Error al obtener los datos del historial:', error);
        }
    }

    // --- LÓGICA PARA EL RANKING DE USUARIOS ---
    function displayUserRanking(data) {
        const userRankingBody = document.getElementById('user-ranking-body');
        if (!userRankingBody) return;

        userRankingBody.innerHTML = '';
        data.forEach((usuario, index) => {
            const row = document.createElement('tr');
            if (index === 0) row.classList.add('rank-1');
            if (index === 1) row.classList.add('rank-2');
            if (index === 2) row.classList.add('rank-3');
            
            row.innerHTML = `<td data-label="Top">${index + 1}</td><td data-label="Usuario">${usuario.usuario}</td><td data-label="Saldo">$${new Intl.NumberFormat('es-CL').format(usuario.saldo)}</td>`;
            userRankingBody.appendChild(row);
        });
    }

    async function fetchUserRanking() {
        try {
            const response = await fetch('/Casino_Local/api/API.php?accion=ranking_usuarios');
            const data = await response.json();
            displayUserRanking(data);
        } catch (error) {
            console.error('Error al obtener los datos del ranking de usuarios:', error);
        }
    }

    // Carga inicial y actualización periódica para ambas tablas
    fetchGameHistory();
    fetchUserRanking();
    setInterval(fetchGameHistory, 5000);
    setInterval(fetchUserRanking, 5000);
});