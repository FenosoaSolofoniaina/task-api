export function CustomBlueInput({ id, ref, type, placeholder, title, required, children }) {

    return (
        <div className="flex flex-col items-start my-[1em]">
            <label htmlFor={id}
                   className="font-bold" >
                {children}
            </label>
            <input type={type}
                    ref={ref}
                    name={id}
                    placeholder={placeholder}
                    id={id}
                    title={title}
                    required={required}
                    className="border rounded-[0.4em] border-[#086288] outline-none py-[0.4em] px-[0.8em] w-[100%] focus:border-[#4D8DBA] caret-[#4D8DBA]"/>
        </div>
    )
}

export function CustomBlueSelect({ id, textLabel, children }) {

    return (
        <div className="flex flex-col items-start my-[1em]" >
            <label htmlFor={id}
                   className="font-bold" >
                {textLabel}
            </label>
            <select name={id}
                    id={id}
                    className="border rounded-[0.4em] border-[#086288] outline-none py-[0.4em] px-[0.8em] w-[100%] focus:border-[#4D8DBA] caret-[#4D8DBA]" >
                {children}   
            </select>
        </div>
    )
}