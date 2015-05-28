<?php
set_time_limit(1800);


$prtcl = "http";
$host = "localhost";
$port = 8000;
$q = "q";
$texto_file = 'london.txt';
$texto = file_get_contents(dirname(__file__).'\\'.$texto_file);
$texto = trim($texto);
$texto = preg_replace('/(\r*\n)+/', ' ', $texto);
$texto = preg_replace('/  +/', ' ', $texto);
$texto = preg_replace('/[^0-9 a-zA-ZáéíóúüñÁÉÍÓÚÜÑ;,_"=\\\&\%\+\*¡¿\!\?\'\#\/\$\[\]\(\)\.\:\-\r\n­]/', '', $texto);
$texto = explode(". ", $texto);
function strposa($haystack, $needles=array(), $offset=0) {
        $chr = array();
        foreach($needles as $needle) {
                $res = strpos($haystack, $needle, $offset);
                if ($res !== false) $chr[$needle] = $res;
        }
        if(empty($chr)) return false;
        return min($chr);
}
function enviarPost($texto) {
  global $prtcl,$host,$port;
  $postdata = http_build_query(
    array(
      'q' => $texto,
      )
    );
  $opts = array('http' =>
    array(
      'method'  => 'POST',
      'header'  => 'Content-type: application/x-www-form-urlencoded',
      'content' => $postdata
      )
    );
  $context  = stream_context_create($opts);
  return file_get_contents("$prtcl://$host:$port/index.php", false, $context);
}
$data = array();
$i = -1;
$txtmem=array();
foreach ($texto as $frase) {
  $frase = trim($frase);
  $i++;
  $txtmem[]=$frase;
  if ($i/10==floor($i/10) || $i==count($texto)-1) {
    //$data = json_decode(enviarPost($texto));
    $data = array_merge($data,json_decode(enviarPost(implode(" ", $txtmem))));
    $txtmem = array();
  }
}
//stopwords
$stopchars = array('+');
for ($i=0; $i < 10 ; $i++) { // no numbers
  $stopchars[] = "$i";
}
$stopwords = array('tener', 'hacia', 'allí', 'de', 'la', 'que', 'el', 'en', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'es', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'fue', 'este', 'ha', 'sí', 'porque', 'esta', 'son', 'entre', 'está', 'cuando', 'muy', 'sin', 'sobre', 'ser', 'tiene', 'también', 'me', 'hasta', 'hay', 'donde', 'han', 'quien', 'están', 'estado', 'desde', 'todo', 'nos', 'durante', 'estados', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'fueron', 'ese', 'eso', 'había', 'ante', 'ellos', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'sea', 'poco', 'ella', 'estar', 'haber', 'estas', 'estaba', 'estamos', 'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosotros', 'vosotras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está', 'estamos', 'estáis', 'están', 'esté', 'estés', 'estemos', 'estéis', 'estén', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 'estaríamos', 'estaríais', 'estarían', 'estaba', 'estabas', 'estábamos', 'estabais', 'estaban', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras', 'estuviéramos', 'estuvierais', 'estuvieran', 'estuviese', 'estuvieses', 'estuviésemos', 'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 'estados', 'estadas', 'estad', 'he', 'has', 'ha', 'hemos', 'habéis', 'han', 'haya', 'hayas', 'hayamos', 'hayáis', 'hayan', 'habré', 'habrás', 'habrá', 'habremos', 'habréis', 'habrán', 'habría', 'habrías', 'habríamos', 'habríais', 'habrían', 'había', 'habías', 'habíamos', 'habíais', 'habían', 'hube', 'hubiste', 'hubo', 'hubimos', 'hubisteis', 'hubieron', 'hubiera', 'hubieras', 'hubiéramos', 'hubierais', 'hubieran', 'hubiese', 'hubieses', 'hubiésemos', 'hubieseis', 'hubiesen', 'habiendo', 'habido', 'habida', 'habidos', 'habidas', 'soy', 'eres', 'es', 'somos', 'sois', 'son', 'sea', 'seas', 'seamos', 'seáis', 'sean', 'seré', 'serás', 'será', 'seremos', 'seréis', 'serán', 'sería', 'serías', 'seríamos', 'seríais', 'serían', 'era', 'eras', 'éramos', 'erais', 'eran', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron', 'fuera', 'fueras', 'fuéramos', 'fuerais', 'fueran', 'fuese', 'fueses', 'fuésemos', 'fueseis', 'fuesen', 'siendo', 'sido', 'tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen', 'tenga', 'tengas', 'tengamos', 'tengáis', 'tengan', 'tendré', 'tendrás', 'tendrá', 'tendremos', 'tendréis', 'tendrán', 'tendría', 'tendrías', 'tendríamos', 'tendríais', 'tendrían', 'tenía', 'tenías', 'teníamos', 'teníais', 'tenían', 'tuve', 'tuviste', 'tuvo', 'tuvimos', 'tuvisteis', 'tuvieron', 'tuviera', 'tuvieras', 'tuviéramos', 'tuvierais', 'tuvieran', 'tuviese', 'tuvieses', 'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido', 'tenida', 'tenidos', 'tenidas', 'tened');
$stopwords2 = array(
  ",","y","-","a","o",".",";",":","¿","?","¡","!","'",'"',"&","+","*","/", "#", "%"
); //"_" no se debe incluír en stopchars por palabras unidas como nombre propios, "al_parecer", etc.

$stopwords = array_unique(array_merge($stopwords,$stopwords2));

//salida como json
$out = array();
foreach ($data as $dat) {
  foreach ($dat as $d) {
    if (strlen($d)>2 && !in_array($d, $stopwords) && !strposa($d, $stopchars))
      $out[]=$d;
  }
}
$out = array_count_values($out);
arsort($out);
header('Content-Type: application/json; charset=utf-8');
#header('Content-Type: text/html; charset=utf-8');
#echo "<html><body><pre>";
echo json_encode($out);
#echo "</pre></html></body>";
exit;



$data = array();
foreach ($texto as $frase) {
	$frase = urlencode(trim($frase));
	$url = "$prtcl://$host:$port/?$q=$frase";
	$data = json_decode(file_get_contents($url));
	flush();
}
echo "<pre>";
print_r($data);
echo "</pre>";
//header('Content-Type: application/json');
//echo $data;
exit;
?>
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Freeling</title>
  <meta name="description" content="Freeling">
  <meta name="author" content="Sanx">

  <!--link rel="stylesheet" href="css/styles.css?v=1.0"-->

  <!--[if lt IE 9]>
  <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
  <![endif]-->
</head>

<body>

<pre>
</pre>

  <!--script src="js/scripts.js"></script-->
</body>
</html>