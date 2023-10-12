$('#pfp').fadeIn();
$('#popup').hide();
$('#del').hide();
$('#edit').hide();
$('#win').hide();
$("td").hide();
$(".index").hide();

$("tr > td").slideDown();
$(".index").slideDown();

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
    $('#popup').show();
    $('#win').fadeIn(200);

    if (req == 'd')
    {
        $('#del').show();
        let prompt = '';
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
        $('#del h2').html(prompt);
    }

    else if (req == 'e')
    {
        $('#edit').show();
    }

    if (details !== "undefined")
    {
        $('#details').html("<p>" + details + "</p>");;
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
    $('#popup').hide();
    $('#win').hide();
}

// new text('h1', 'h2', 'h3', 'p', 'a', 'li')

function darkmode() {
    $('body').css('backgroundColor','#262626');
    $('*').css('color','white');
    $('tr').css('backgroundColor','gray');
}

function lightmode() {
    $('body').css('backgroundColor','white');
    $('*').css('color','black');
}