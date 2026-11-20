import { CustomH2MediumTitle } from '../components/Titles';
import { CustomRedButton } from '../components/Buttons';

import { FooterLayout } from '../layouts/Footer';
import { HeaderLayout } from '../layouts/Header';
import { BodyLayout } from '../layouts/Body';



export default function Dashboard() {

    function logout(e) {
        e.preventDefault();
        console.log("Deconnection...");

    }

    return (
        <>
            <HeaderLayout />
            
            <BodyLayout>
                <CustomH2MediumTitle>
                    Bienvenue sur votre dashboard personnel de Task Manager
                </CustomH2MediumTitle>
                <p>
                    Lorem ipsum dolor sit, amet consectetur adipisicing elit. Beatae excepturi cupiditate error! Distinctio nulla, illo est eaque nam reiciendis voluptatem explicabo similique exercitationem a. Architecto qui ad natus obcaecati quasi.
                </p>
                <CustomRedButton title="Se déconnecter" onClick={logout}>
                    Se déconnecter
                </CustomRedButton>
            </BodyLayout>

            <FooterLayout />
        </>
    );
}