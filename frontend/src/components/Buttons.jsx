export function CustomBlueSubmitButton({ children }) {
    
    return (
        <button type="submit"
                className="rounded-[0.4em] text-white bg-[#086288] py-[0.4em] px-[0.8em] w-[100%] hover:bg-[#4D8DBA] click:bg-[#4D8DBA]" >
            {children}
        </button>
    );

}


export function CustomBlueButton({ onClick, children }) {
    
    return (
        <button type="button"
                onClick={onClick}
                className="rounded-[0.4em] text-white bg-[#086288] py-[0.4em] px-[0.8em] w-[100%] hover:bg-[#4D8DBA] click:bg-[#4D8DBA]" >
            {children}
        </button>
    );

}