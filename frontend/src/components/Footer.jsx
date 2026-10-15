function Footer() {

    return (
        <footer className="flex flex-row justify-between gap-x-[3em] font-medium text-dark-800 py-[2em] px-[1em]" >
            <h3 className="text-[1em]" >
                Task Manager App
            </h3>
            <p className="text-[1em]" >
                Organiser vos tâches comme si c'était un jeu (un jeu amusant)
            </p>
            <p className="text-[0.9em]" >
                <strong> Fenosoa </strong>
                &copy; 2026
            </p>
        </footer>
    );
}

export default Footer;