import { Link } from 'react-router';


export function CustomBlueLink({ hrefLink, title, children }) {

    return (
        <Link to={hrefLink}
            className="font-medium text-[1em] text-[#086288] mx-[0.5em] cursor-pointer hover:text-[#4D8DBA] click:text-[#4D8DBA]" 
            title={title} >
            {children}
        </Link>
    );
}