$('#pfp').fadeIn();

const qte = document.getElementsByClassName('qte');
for (let i=0; i < qte.length; i++)
{
    if (qte[i].innerHTML == '0')
    {
        qte[i].parentElement.style.backgroundColor = "#ff9999";
        qte[i].style.backgroundColor = "#ff6666";
    }
}


const stat = document.getElementsByClassName('stat');

for (let i=0; i < stat.length; i++)
{
    if (stat[i].innerHTML == 'Traité')
    {
        stat[i].parentElement.style.backgroundColor = "#66ff66";
        stat[i].style.backgroundColor = "#00e64d";
    }
    else
    {
        stat[i].parentElement.style.backgroundColor = "#ff9999";
        stat[i].style.backgroundColor = "#ff6666";
    }
}

function popup(req, name, type, details)
{
    pop = document.getElementById('popup');
    factpop = document.getElementById('factpop');
    factcont = document.getElementById('factcontent');
    del = document.getElementById('del');
    edit = document.getElementById('edit');

    win = document.getElementById("win");
    win.style.animation = "fadeIn 0.5s";

    if (req == 'd')
    {
        pop.style.display = "block";
        let prompt = '';
        del.style.display = "inline-block";
        delprompt = document.querySelector("#del h2");
        if (type == 'p')
        {
            prompt = "Voulez-vous vraiment supprimer le produit '" + name + "' ?";
        }
        else if (type == 'l')
        {
            prompt = "Voulez-vous vraiment supprimer la commande " + name + " ?";
        }
        else if (type == 'f')
        {
            prompt = "Voulez-vous vraiment supprimer la facture " + name + " ?";
        }
        delprompt.innerHTML = prompt;
    }

    else if (req == 'e')
    {
        edit.style.display = "block";
    }

    if (details !== "undefined")
    {
        det = document.getElementById("details");
        det.innerHTML = "<p>" + details + "</p>"
    }
}

function showfactpop(id, label, pu, qte) 
{
    pop = document.getElementById('popup');
    factpop = document.getElementById('factpop');
    factcont = document.getElementById('factcontent');

    factpop.style.display = "inline-block";
    factcont.innerHTML = "<p>" + id + "</p>";
    alert(row);
}

function closepopup() {
    pop = document.getElementById('popup');
    win = document.getElementById("win");
    win.style.animation = "fadeOut 0.5s";
    pop.style.display = "none";
}
