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

        data.forEach((partida) => {
            const row = document.createElement('tr');
            
            let resultadoClase = '';
            let resultadoTexto = '';

            switch (partida.resultado) {
                case 'ganaste':
                    resultadoClase = 'resultado-ganaste';
                    resultadoTexto = 'Ganó';
                    break;
                case 'perdiste':
                    resultadoClase = 'resultado-perdiste';
                    resultadoTexto = 'Perdió';
                    break;
                case 'empate':
                    resultadoClase = 'resultado-empate';
                    resultadoTexto = 'Empate';
                    break;
                default:
                    resultadoTexto = partida.resultado;
            }

            // --- FORMATEO DE FECHA Y HORA (Día/Mes Hora:Minuto) ---
            const fecha = new Date(partida.fecha);

            const dia = String(fecha.getDate()).padStart(2, '0');
            const mes = String(fecha.getMonth() + 1).padStart(2, '0'); // Se suma 1 porque los meses van de 0 a 11
            const hora = String(fecha.getHours()).padStart(2, '0');
            const minutos = String(fecha.getMinutes()).padStart(2, '0');

            const fechaFormateada = `${dia}/${mes} ${hora}:${minutos}`;
            
            // Contenido de la fila actualizado con la nueva fecha
            row.innerHTML = `
                <td>${fechaFormateada}</td>
                <td>${partida.usuario}</td> 
                <td>${partida.apuesta}</td>
                <td>${partida.nombre_juego}</td>
                <td><span class="${resultadoClase}">${resultadoTexto}</span></td>
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

        } catch (error)
        {
            console.error('Error al obtener los datos del ranking:', error);
            const rankingBody = document.getElementById('ranking-body');
            if (rankingBody) {
                rankingBody.innerHTML = '<tr><td colspan="5">No se pudo cargar el historial.</td></tr>';
            }
        }
    }

    fetchRanking();
});