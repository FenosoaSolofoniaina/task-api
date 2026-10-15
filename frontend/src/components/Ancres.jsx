import { Link } from 'react-router';


export function CustomBlueLink({ hrefLink, title, children }) {

    return (
        <Link to={hrefLink}
              className="font-medium text-[1em] text-[#086288] hover:text-[#4D8DBA] click:text-[#4D8DBA] cursor-pointer" 
              title={title} >
            {children}
        </Link>
    );
}