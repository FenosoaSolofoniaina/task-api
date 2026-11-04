import { CustomBlueLink } from "../components/Ancres"



export function BodyLayout({ children }) {
    
    return (
        <div className="flex flex-row justify-center" >
            <div className="flex flex-col text-center border border-1 border-[#086288] rounded-[1em] bg-white w-[50%] p-[3em] gap-y-[2em]" >
                {children}
            </div>
        </div>
    )
}


export function AccountOption({ linkOption, children }) {
    
    return (
        <div className="flex flex-row justify-center items-center my-[0.3em]" >
            {children}
            <CustomBlueLink
                hrefLink={linkOption.href}
                title={linkOption.text} >
                    {linkOption.text}
            </CustomBlueLink>
        </div>
    );
}