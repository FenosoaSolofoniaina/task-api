export function CustomBlueSubmitButton({ title, children }) {
    
    return (
        <button type="submit"
                title={title}
                className="rounded-[0.4em] text-white bg-[#086288] py-[0.4em] px-[0.8em] w-[100%] hover:bg-[#4D8DBA] click:bg-[#4D8DBA]" >
            {children}
        </button>
    );

}


export function CustomBlueButton({ title, onClick, children }) {
    
    return (
        <button type="button"
                title={title}
                onClick={onClick}
                className="rounded-[0.4em] text-white bg-[#086288] py-[0.4em] px-[0.8em] w-[100%] hover:bg-[#4D8DBA] click:bg-[#4D8DBA]" >
            {children}
        </button>
    );

}


export function CustomRedButton({ title, onClick, children }) {
    
    return (
        <button type="button"
                title={title}
                onClick={onClick}
                className="rounded-[0.4em] text-white bg-[#E63946] py-[0.4em] px-[0.8em] w-[100%] hover:bg-[#8B1E2D] click:bg-[#8B1E2D]" >
            {children}
        </button>
    );

}