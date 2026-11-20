export function CustomBlueInput({ id, type, label, title, value, required, errorMessage=null, onChange }) {

    return (
        <div className="flex flex-col items-start my-[1em]">
            <label htmlFor={id}
                   className="font-bold" >
                {label}
                { required && <b className="text-red-500">*</b> }
            </label>
            <input type={type}
                    id={id}
                    name={id}
                    title={title}
                    value={value}
                    onChange={onChange}
                    required={required}
                    className="border rounded-[0.4em] border-[#086288] outline-none py-[0.4em] px-[0.8em] w-[100%] focus:border-[#4D8DBA] caret-[#4D8DBA]"/>
            { errorMessage && <p className="text-[0.8em] font-medium text-[#FF0000]">{errorMessage}</p> }
        </div>
    )
}


export function CustomBlueCheckBox({ id, label, value, onChange }) {

    return (
        <div className="flex flex-row justify-start gap-[0.3em]" >
            <input type="checkbox"
                    id={id}
                    name={id}
                    value={value}
                    onChange={onChange}
            />
            <label htmlFor={id}
                   className="font-medium" >
                {label}
            </label>
        </div>
    )
}


export function CustomBlueRadio({ id, name, value, checked, label, onChange }) {

    return (
        <div className="flex flex-row justify-start gap-[0.3em]" >
            <input type="radio"
                    id={id}
                    name={name}
                    value={value}
                    checked={checked}
                    onChange={onChange}
            />
            <label htmlFor={id}
                   className="font-medium" >
                {label}
            </label>
        </div>
    )
}



export function CustomBlueSelect({ id, textLabel, onChange, children }) {

    return (
        <div className="flex flex-col items-start my-[1em]" >
            <label htmlFor={id}
                   className="font-bold" >
                {textLabel}
            </label>
            <select name={id}
                    id={id}
                    onChange={onChange}
                    className="border rounded-[0.4em] border-[#086288] outline-none py-[0.4em] px-[0.8em] w-[100%] focus:border-[#4D8DBA] caret-[#4D8DBA]" >
                {children}   
            </select>
        </div>
    )
}