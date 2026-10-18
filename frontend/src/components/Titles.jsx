export function CustomH2MediumTitle({ children }) {

    return (
        <h2 className="text-[1.5em] font-medium" >
            {children}
        </h2>
    );
}

export function CustomH3MediumTitle({ children }) {

    return (
        <h3 className="text-[1em] font-medium" >
            {children}
        </h3>
    );
}

export function CustomErrorTitle({ children }) {

    return (
        <h3 className="text-[1em] font-bold text-[#FF0000]" >
            {children}
        </h3>
    );
}