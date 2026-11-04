import { CustomH2MediumTitle } from '../components/Titles';
import { CustomBlueLink } from '../components/Ancres';

import { FooterLayout } from '../layouts/Footer';
import { HeaderLayout } from '../layouts/Header';
import { BodyLayout } from '../layouts/Body';



export default function ErrorPage() {

    return (
        <>
            <HeaderLayout />
            
            <BodyLayout>
                <CustomH2MediumTitle>
                    Oups: Une erreur s'est produite de notre côté.
                    Veuillez réessayer plus tard ou revenir
                    en <CustomBlueLink hrefLink="/" > page d'accueil </CustomBlueLink>
                </CustomH2MediumTitle>
            </BodyLayout>

            <FooterLayout />
        </>
    );
}