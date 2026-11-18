import { CustomH2MediumTitle } from '../components/Titles';
import { CustomBlueLink } from '../components/Ancres';

import { FooterLayout } from '../layouts/Footer';
import { HeaderLayout } from '../layouts/Header';
import { BodyLayout } from '../layouts/Body';



export default function IndexPage() {

    return (
        <>
            <HeaderLayout />

            <BodyLayout> 
                <CustomH2MediumTitle>
                    Bienvenue sur Task Manager App
                </CustomH2MediumTitle>
                <p className="text-[1em]">
                    Lorem ipsum dolor sit amet consectetur, adipisicing elit. Soluta saepe illum beatae alias sit, delectus rerum facilis omnis enim eaque sint harum! Recusandae velit deserunt consequatur eaque quisquam, odit porro.
                </p>
                <CustomBlueLink hrefLink="/login"
                    title="Se connecter">
                        Se connecter
                </CustomBlueLink>
                <CustomBlueLink hrefLink="/register"
                    title="Créer un compte">
                        Créér un compte
                </CustomBlueLink>
            </BodyLayout>
            
            <FooterLayout />
        </>
    );
}